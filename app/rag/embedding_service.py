from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> np.ndarray:
        embedding = self.model.encode(text)
        return embedding

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts)
        return embeddings
