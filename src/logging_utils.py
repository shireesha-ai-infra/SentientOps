import logging

LOG_FILE = "rag_system.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Helper logging functions

def log_query(question: str):
    logger.info(f"USER QUESTION: {question}")

def log_chunks(chunk_ids):
    logger.info(f"RETRIVED CHUNKS: {chunk_ids}")

def log_latency(latency: float):
    logger.info(f"LATENCY: {latency:.3f} seconds")

def log_output(answer:str):
    logger.info(f"OUTPUT: {answer}")

def log_msg(msg:str):
    logger.info(f"{msg}")