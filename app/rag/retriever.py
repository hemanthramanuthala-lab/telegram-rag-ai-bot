from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.store = VectorStore()

    def index_documents(self, documents):
        if not documents:
            return

        embeddings = self.embedder.embed_texts(documents)
        self.store.add_embeddings(embeddings, documents)

    def retrieve(self, query, top_k=2):
        if not self.store.text_chunks:
            return []

        query_vector = self.embedder.embed_text(query)

        results = self.store.search(
            query_vector,
            top_k=top_k
        )

        # 🔥 FIX: Extract only text from (text, score)
        cleaned_results = []

        for item in results:
            if isinstance(item, tuple):
                cleaned_results.append(item[0])
            else:
                cleaned_results.append(item)

        return cleaned_results
