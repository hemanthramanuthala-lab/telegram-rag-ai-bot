from fastapi import FastAPI, Request
from dotenv import load_dotenv
from telegram import Update
from app.bot import create_telegram_app

load_dotenv()

app = FastAPI()

telegram_app = create_telegram_app()

@app.on_event("startup")
async def startup():
    await telegram_app.initialize()
    await telegram_app.start()

@app.on_event("shutdown")
async def shutdown():
    await telegram_app.stop()
    await telegram_app.shutdown()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "Telegram AI Bot (Webhook Mode)"}
