from typing import List
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def index_documents(self, texts: List[str]):
        embeddings = self.embedding_service.embed_texts(texts)
        self.vector_store.add_embeddings(embeddings, texts)

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        query_embedding = self.embedding_service.embed_text(query)
        results = self.vector_store.search(query_embedding, top_k)
        return results
