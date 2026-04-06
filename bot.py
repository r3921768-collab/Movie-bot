import telebot
import time
import os
from flask import Flask
from threading import Thread

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

SOURCE_CHANNEL = -1003867813389  # database
TARGET_CHANNEL = "@ITQ5AVAT3FYWNWJL"  # main
MESSAGE_ID = 213  # movie id

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    while True:
        try:
            bot.forward_message(
                chat_id=TARGET_CHANNEL,
                from_chat_id=SOURCE_CHANNEL,
                message_id=MESSAGE_ID
            )
            time.sleep(300)  # 5 min gap
        except Exception as e:
            print("ERROR:", e)
            time.sleep(10)

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
