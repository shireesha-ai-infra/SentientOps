from src.ingest import load_pdfs
from src.embed import create_embeddings, model
from src.retrieve import VectorStore
from src.generate import generate_answer
from src.logging_utils import log_chunks, log_query, log_latency, log_output
from time import time
from src.metrics import (
    record_request,
    record_latency,
    record_retrieval_time,
    record_generation_time
)
import pickle
import os
from src.cache import get_cached_answer, set_cached_answer

VECTOR_STORE_PATH = "data/vector_store.pkl"
CHUNKS_PATH = "data/chunks.pkl"
PDF_DIR = "data/pdf_files"

def build_rag_pipeline(pdf_dir:str):

    if os.path.exists(VECTOR_STORE_PATH) and os.path.exists(CHUNKS_PATH):
        with open(VECTOR_STORE_PATH, "rb") as f:
            store = pickle.load(f)
        with open(CHUNKS_PATH, "rb") as f:
            chunks = pickle.load(f)
    
    else:
        # Data Ingestion
        texts = load_pdfs(PDF_DIR)

        # Create Embeddings
        chunks, embeddings = create_embeddings(texts)

        # Store the embeddings in vector DB
        store = VectorStore(embeddings)

    return chunks, store


def ask(question:str, chunks, store):
    # --- Checking Cache first ------
    cached = get_cached_answer(question)
    if cached is not None:
        return {
            "answer": cached,
            "latency_seconds": 0.0,
            "retrieval_time_seconds": 0.0,
            "generation_time_seconds": 0.0,
            "cached": True
        }
    

    start_time = time()
    
    # ----- request count -------
    record_request()
    log_query(question)

    # ------- Retrieval Timing ----------
    t1 = time()
    # creating embeddings for query
    query_emb = model.encode(question)

    # Retrieve (by semantic search)
    indices = store.search(query_emb)
    retrieval_time = time() - t1
    record_retrieval_time(retrieval_time)

    log_chunks(indices.tolist())

    # ------- Generation Timing ------
    t2 = time()
    context = [chunks[i] for i in indices]
    answer = generate_answer(context, question)
    generation_time = time() - t2
    record_generation_time(generation_time)

    # log_output(answer.strip())

    latency = time() - start_time
    record_latency(latency)
    log_latency(latency)

    # ----- Save in cache -------
    set_cached_answer(question, answer.strip())

    return {
        "answer": answer.strip(), 
        "latency_seconds": latency,
        "retrieval_time_seconds": retrieval_time,
        "generation_time_seconds": generation_time,
        "cached": False
    }