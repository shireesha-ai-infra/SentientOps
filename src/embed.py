from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(texts, chunk_sixe=500):
    chunks = []
    for text in texts:
        for i in range(0, len(text), chunk_sixe):
            chunks.append(text[i:i+chunk_sixe])

    embeddings = model.encode(chunks)
    return chunks,embeddings
