import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from app.handlers import handle_message, handle_document


def create_telegram_app():
    telegram_token = os.getenv("TELEGRAM_TOKEN")

    telegram_app = ApplicationBuilder().token(telegram_token).build()

    # Document handler FIRST
    telegram_app.add_handler(
        MessageHandler(filters.Document.ALL, handle_document)
    )

    # Text messages
    telegram_app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    return telegram_app
