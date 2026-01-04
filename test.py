from src.ingest import load_pdfs
from src.embed import create_embeddings

# Data Ingestion
texts = load_pdfs("data/pdf_files")

# Create Embeddings
chunks, embeddings = create_embeddings(texts)


print(len(texts))
print(len(chunks))
print(embeddings.shape)