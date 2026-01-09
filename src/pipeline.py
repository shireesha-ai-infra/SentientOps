from src.ingest import load_pdfs
from src.embed import create_embeddings, model
from src.retrieve import VectorStore
from src.generate import generate_answer
from src.logging_utils import log_chunks, log_query, log_latency, log_output
import time

def build_rag_pipeline(pdf_dir:str):
    # One-time setup
    # Data Ingestion
    texts = load_pdfs("data/pdf_files")

    # Create Embeddings
    chunks, embeddings = create_embeddings(texts)

    # Store the embeddings in vector DB
    store = VectorStore(embeddings)

    return chunks, store


def ask(question:str, chunks, store):
    start_time = time.time()

    log_query(question)

    # creating embeddings for query
    query_emb = model.encode(question)

    # Retrieve (by semantic search)
    indices = store.search(query_emb)
    log_chunks(indices.tolist())

    context = [chunks[i] for i in indices]
    answer = generate_answer(context, question)

    # log_output(answer.strip())

    latency = time.time() - start_time
    log_latency(latency)

    return {
        "answer": answer.strip(), 
        "latency": latency
    }