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
    record_request,
    record_latency,
    record_generation_time,
    record_retrieval_time,
    record_cache_hit,
    record_tokens,
    record_rejection,
    COST_PER_1K_TOKENS
)
from src.cache import get_cached_answer, set_cached_answer
from src.timeouts import run_with_timeout, TimeoutException
from src.fallbacks import (
    no_context_fallback, 
    generation_error_fallback, 
    system_error_fallback
)

from src.prometheus_metrics import (
    requests_total,
    cache_hits,
    rejections,
    latency,
    retrieval_time,
    generation_time,
    llm_cost,
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
        record_cache_hit()
        requests_total.inc()              
        latency.set(0.0)                  
        retrieval_time.set(0.0)          
        generation_time.set(0.0)
        return {
            "answer": cached,
            "latency_seconds": 0.0,
            "retrieval_time_seconds": 0.0,
            "generation_time_seconds": 0.0,
            "cached": True
        }
    
    requests_total.inc()
    record_request()
    start_time = time()

    try:
        # ----- request logging -------
        log_query(question)

        # ------- Retrieval  ----------
        t1 = time()
        # creating embeddings for query
        query_emb = model.encode(question)

        # Retrieve (by semantic search)
        indices, similarities = store.search(query_emb)
        retrieval_time_value = time() - t1
        record_retrieval_time(retrieval_time_value)
        retrieval_time.set(retrieval_time_value)  


        log_chunks(indices.tolist())

        # ------ Empty Retrieval handling ------
        if len(indices) == 0:
            answer = no_context_fallback(question)
            latency_value = time() - start_time
            record_latency(latency_value)
            latency.set(latency_value) 

            return {
                "answer": answer,
                "latency_seconds": latency_value,
                "retrieval_time_seconds": retrieval_time_value,
                "generation_time_seconds": 0.0,
                "cached": False,
            }
        """
        # ---- Grounding Gate ----
        MAX_SIMILARITY = max(similarities)

        RELEVANCE_THRESHOLD = 0.30   # tune this

        if MAX_SIMILARITY < RELEVANCE_THRESHOLD:
            record_rejection()
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
            gen_time_val = time() - t2
            generation_time.set(gen_time_val) 
        except TimeoutException:
            answer = generation_error_fallback()
            gen_time_val = 0.0
        
        approx_tokens = len(answer.split()) * 1.3
        record_tokens(approx_tokens)
        current_cost = (approx_tokens / 1000) * COST_PER_1K_TOKENS
        llm_cost.set(current_cost) 




        record_generation_time(gen_time_val)

        # log_output(answer.strip())

        # ---- Final Latency -------------
        latency_val = time() - start_time
        record_latency(latency_val)
        latency.set(latency_val)

        log_latency(latency_val)

        # ----- Save in cache -------
        set_cached_answer(question, answer.strip())

        return {
            "answer": answer.strip(), 
            "latency_seconds": latency_val,
            "retrieval_time_seconds": retrieval_time_value,
            "generation_time_seconds": gen_time_val,
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