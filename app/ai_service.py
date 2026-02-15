import os
from groq import Groq

SYSTEM_PROMPT = """
You are a professional AI assistant.
Give clear, structured, and accurate answers.
"""

def generate_ai_response(user_text: str) -> str:
    groq_api_key = os.getenv("GROQ_API_KEY")

    groq_client = Groq(api_key=groq_api_key)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text}
    ]

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    return response.choices[0].message.content
