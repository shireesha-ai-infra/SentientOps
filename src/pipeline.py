import pickle
import os
from time import time

from src.ingest import load_pdfs
from src.embed import create_embeddings, model
from src.retrieve import VectorStore
from src.generate import generate_answer

from src.logging_utils import (
    log_chunks, 
    log_query, 
    log_latency, 
    log_output,
    log_msg
)

from src.metrics import (
    record_request,
    record_latency,
    record_retrieval_time,
    record_generation_time
)
from src.cache import get_cached_answer, set_cached_answer
from src.timeouts import run_with_timeout, TimeoutException
from src.fallbacks import (
    no_context_fallback, 
    generation_error_fallback, 
    system_error_fallback
)

VECTOR_STORE_PATH = "data/vector_store.pkl"
CHUNKS_PATH = "data/chunks.pkl"
PDF_DIR = "data/pdf_files"

def build_rag_pipeline(pdf_dir:str):
    if os.path.exists(VECTOR_STORE_PATH) and os.path.exists(CHUNKS_PATH):
        with open(VECTOR_STORE_PATH, "rb") as f:
            store = pickle.load(f)
        with open(CHUNKS_PATH, "rb") as f:
            chunks = pickle.load(f)
        
        print("✅ Loaded vector store from disk")

    
    else:
        print("⚠️ No vector store found, building new index")

        # Data Ingestion
        texts = load_pdfs(PDF_DIR)

        # Create Embeddings
        chunks, embeddings = create_embeddings(texts)        

        # Store the embeddings in vector DB
        store = VectorStore(embeddings)
    return chunks, store


def ask(question:str, chunks, store):
    # ----- Cache check --------
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

    try:
        # ----- request logging -------
        record_request()
        log_query(question)

        # ------- Retrieval  ----------
        t1 = time()
        # creating embeddings for query
        query_emb = model.encode(question)

        # Retrieve (by semantic search)
        indices, similarities = store.search(query_emb)
        retrieval_time = time() - t1
        record_retrieval_time(retrieval_time)

        log_chunks(indices.tolist())

        # ------ Empty Retrieval handling ------
        if len(indices) == 0:
            answer = no_context_fallback(question)
            latency = time() - start_time
            record_latency(latency)
            return {
                "answer": answer,
                "latency_seconds": latency,
                "retrieval_time_seconds": retrieval_time,
                "generation_time_seconds": 0.0,
                "cached": False,
            }
        """
        # ---- Grounding Gate ----
        MAX_SIMILARITY = max(similarities)

        RELEVANCE_THRESHOLD = 0.30   # tune this

        if MAX_SIMILARITY < RELEVANCE_THRESHOLD:
            answer = no_context_fallback(question)
            latency = time() - start_time
            record_latency(latency)
            return {
                "answer": answer,
                "latency_seconds": latency,
                "retrieval_time_seconds": retrieval_time,
                "generation_time_seconds": 0.0,
            }
        """
        
        # ------- Generation (with Timeout and only if grounded) --------        
        t2 = time()
        context = [chunks[i] for i in indices]

        def generate():
            return generate_answer(context, question)
        
        try:
            answer = generate_answer(context, question)
            generation_time = time() - t2
        except TimeoutException:
            answer = generation_error_fallback()
            generation_time = 0.0


        record_generation_time(generation_time)

        # log_output(answer.strip())

        # ---- Final Latency -------------
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
    except Exception as e:
        # Log unexpected failure
        log_output(f"ERROR: {str(e)}")

        answer = system_error_fallback()
        return {
            "answer": answer.strip(), 
            "latency_seconds": time() - start_time,
            "retrieval_time_seconds": 0.0,
            "generation_time_seconds": 0.0,
            "cached": False
        }