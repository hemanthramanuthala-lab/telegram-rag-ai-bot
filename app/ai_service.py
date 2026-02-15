import os
from groq import Groq
from app.rag.retriever import Retriever
from app.rag.chunker import TextChunker


SYSTEM_PROMPT = """
You are a friendly AI assistant.

You can:
- Chat casually
- Tell jokes
- Answer general knowledge
- Answer based on uploaded documents

RULES:
- If document context is provided, answer ONLY from that context.
- If document context exists, do NOT use outside knowledge.
- If no document context, you can answer normally.
- Be friendly and conversational.
"""


class AIService:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        self.retriever = Retriever()
        self.chunker = TextChunker()

        self.base_loaded = False

        self._load_base_knowledge()

    # -----------------------------
    # Load base knowledge once
    # -----------------------------
    def _load_base_knowledge(self):
        if self.base_loaded:
            return

        if not os.path.exists("data/knowledge.txt"):
            return

        with open("data/knowledge.txt", "r") as f:
            text = f.read()

        chunks = self.chunker.chunk(text)
        self.retriever.index_documents(chunks)

        self.base_loaded = True

    # -----------------------------
    # Add uploaded document
    # -----------------------------
    def add_uploaded_document(self, text):
        chunks = self.chunker.chunk(text)
        self.retriever.index_documents(chunks)

    # -----------------------------
    # Generate Response
    # -----------------------------
    def generate_response(self, user_id, user_message):

        # Step 1: Retrieve context
        retrieved_chunks = self.retriever.retrieve(user_message)

        if retrieved_chunks:
            context_text = "\n\n".join(retrieved_chunks)

            prompt = f"""
Document Context:
{context_text}

User Question:
{user_message}

Answer using ONLY the document context above.
"""

        else:
            prompt = user_message

        # Step 2: Call Groq
        completion = self.groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        return completion.choices[0].message.content
