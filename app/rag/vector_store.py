import faiss
import numpy as np
from typing import List


class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents: List[str] = []

    def add_embeddings(self, embeddings: np.ndarray, texts: List[str]):
        if len(embeddings.shape) == 1:
            embeddings = np.array([embeddings])

        self.index.add(embeddings)
        self.documents.extend(texts)

    def search(self, query_embedding: np.ndarray, top_k: int = 3):
        if len(query_embedding.shape) == 1:
            query_embedding = np.array([query_embedding])

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results
