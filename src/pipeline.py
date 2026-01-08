from ingest import load_pdfs
from embed import create_embeddings, model
from retrieve import VectorStore
from generate import generate_answer

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
    # creating embeddings for query
    query_emb = model.encode(question)

    # Retrieve (by semantic search)
    indices = store.search(query_emb)

    context = [chunks[i] for i in indices]
    answer = generate_answer(context, question)

    return answer.strip()

if __name__ == "__main__":
    # Build pipeline once
    chunks, store = build_rag_pipeline("data/pdf_files")


    # Query for search
    query = 'What is this document about?'

    output = ask(query, chunks, store)

    print(f"\n Query: {query}")
    print(f"\n Output: {output}")