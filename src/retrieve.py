# Store (Vector DB) & Retrive (Vector Search)

import faiss
import numpy as np

class VectorStore:
    def __init__(self, embeddings):
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.embeddings = embeddings

    def search(self, query_embedding, k=3):
        distances, indices = self.index.search(
            np.array([query_embedding]),k
        )
        return indices[0]
        