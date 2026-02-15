import os
from telegram import Update
from telegram.ext import ContextTypes
from pypdf import PdfReader

# DO NOT import AIService at top level
from app.ai_service import AIService

# Global variable (will be injected from main.py)
ai_service = None


def set_ai_service(service: AIService):
    global ai_service
    ai_service = service


def get_ai_service():
    return ai_service


# ----------------------------
# Handle text messages
# ----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = get_ai_service()

    user_text = update.message.text
    user_id = str(update.message.from_user.id)

    answer = service.generate_response(user_id, user_text)

    await update.message.reply_text(answer)


# ----------------------------
# Handle uploaded documents
# ----------------------------
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = get_ai_service()

    document = update.message.document
    file = await context.bot.get_file(document.file_id)

    os.makedirs("data", exist_ok=True)
    file_path = f"data/{document.file_name}"

    await file.download_to_drive(file_path)

    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    service.add_uploaded_document(text)

    await update.message.reply_text(
        "📄 Document received! I've learned from it. Ask me anything about it 😄"
    )
