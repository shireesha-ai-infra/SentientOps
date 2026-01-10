from src.ingest import load_pdfs
from src.embed import create_embeddings
from src.retrieve import VectorStore
import pickle
import os
from src.pipeline import VECTOR_STORE_PATH, CHUNKS_PATH, PDF_DIR

def rebuild_index():
    print("Re-indexing started...")

    texts = load_pdfs(PDF_DIR)
    chunks, embeddings = create_embeddings(texts)

    store = VectorStore(embeddings)

    # Save Artifacts
    os.makedirs("data", exist_ok=True)
    with open(VECTOR_STORE_PATH, "wb") as f:
        pickle.dump(store, f)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Indexed {len(chunks)} chunks")

    print("Re-indexing completed successfully")

if __name__ == "__main__":
    rebuild_index()