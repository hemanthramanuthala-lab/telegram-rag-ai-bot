from telegram import Update
from telegram.ext import ContextTypes
from app.ai_service import generate_ai_response

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    answer = generate_ai_response(user_text)

    await update.message.reply_text(answer)
