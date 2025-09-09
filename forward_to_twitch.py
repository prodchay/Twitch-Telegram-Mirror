import os
from dotenv import load_dotenv
from telegram import Bot as TelegramBot, Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests

load_dotenv()

print("=================\n" 
"Telegram => Twitch-Forwarder\n" 
"=================")

TELEGRAM_TOKEN = os.getenv("telegram_token")
TELEGRAM_CHAT_ID = int(os.getenv("telegram_chat_id"))

TWITCH_OAUTH = os.getenv("forward_to_telegram_oauth").lstrip("oauth:")

telegram_bot = TelegramBot(token=TELEGRAM_TOKEN)

def send_to_twitch(msg):
    url = "https://api.twitch.tv/helix/chat/messages"
    headers = {
        "Authorization": f"Bearer {TWITCH_OAUTH}",
        "Client-Id": os.getenv("forward_to_telegram_client_id"),
        "Content-Type": "application/json"
    }
    data = {
        "broadcaster_id": os.getenv("twitch_broadcaster_id"),
        "sender_id": os.getenv("twitch_sender_id"),
        "message": msg
    }
    r = requests.post(url, headers=headers, json=data)

    # print(, r.status_code, r.text) # check if something isn't working

async def forward_to_twitch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == TELEGRAM_CHAT_ID:
        msg = update.message.text
        send_to_twitch(f"{msg}")

telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
telegram_app.add_handler(MessageHandler(filters.ALL, forward_to_twitch))

telegram_app.run_polling()
