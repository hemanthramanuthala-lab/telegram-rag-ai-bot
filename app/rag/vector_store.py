import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.text_chunks = []

    def add_embeddings(self, embeddings, text_chunks):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.text_chunks.extend(text_chunks)

    def search(self, query_embedding, top_k=1):  # reduced from 3 → 1
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(
            query_embedding.reshape(1, -1), top_k
        )

        results = []

        for i, idx in enumerate(indices[0]):
            if idx < len(self.text_chunks):
                score = distances[0][i]
                results.append((self.text_chunks[idx], score))

        return results
