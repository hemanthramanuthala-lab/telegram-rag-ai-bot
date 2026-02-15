from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.bot import create_telegram_app
from app.ai_service import AIService
from app.handlers import set_ai_service

# Load environment variables FIRST
load_dotenv()

app = FastAPI()

telegram_app = create_telegram_app()

USE_WEBHOOK = False  # keep polling mode for now


@app.on_event("startup")
async def startup():
    # Create AIService AFTER dotenv loads
    service = AIService()
    set_ai_service(service)

    await telegram_app.initialize()
    await telegram_app.start()

    if not USE_WEBHOOK:
        await telegram_app.updater.start_polling()


@app.on_event("shutdown")
async def shutdown():
    if not USE_WEBHOOK:
        await telegram_app.updater.stop()

    await telegram_app.stop()
    await telegram_app.shutdown()


@app.get("/")
def home():
    return {"message": "Telegram AI Bot Running 🚀"}
