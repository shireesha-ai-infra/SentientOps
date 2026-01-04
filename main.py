from src.ingest import load_pdfs
from src.embed import create_embeddings, model
from src.retrieve import VectorStore
from src.generate import generate_answer

# Data Ingestion
texts = load_pdfs("data/pdf_files")

# Create Embeddings
chunks, embeddings = create_embeddings(texts)

# Query for search
query = 'What is this document about?'

# creating embeddings for query
query_emb = model.encode(query)

# Store the embeddings in vector DB
store = VectorStore(embeddings)

# Retrieve (by semantic search)
indices = store.search(query_emb)


print(len(texts))
print(len(chunks))
print(embeddings.shape)
print(query_emb.shape)

for i in indices:
    print(chunks[i][:500])

def ask(question):
    query_emb = model.encode(question)
    idxs = store.search(query_emb)

    context = [chunks[i] for i in idxs]
    answer = generate_answer(context, question)

    return answer

if __name__ == "__main__":
    print(ask("summarize the document"))