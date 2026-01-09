import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_query(question: str):
    logging.info(f"USER QUESTION: {question}")

def log_chunks(chunk_ids):
    logging.info(f"RETRIVED CHUNKS: {chunk_ids}")

def log_latency(latency: float):
    logging.info(f"LATENCY: {latency:.3f} seconds")