import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from app.handlers import handle_message

def create_telegram_app():
    telegram_token = os.getenv("TELEGRAM_TOKEN")

    if not telegram_token:
        raise ValueError("TELEGRAM_TOKEN is not set in environment variables.")

    app = ApplicationBuilder().token(telegram_token).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    return app
