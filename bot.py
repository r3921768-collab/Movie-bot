import telebot
import time
import os
from flask import Flask
from threading import Thread

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
channel_username = "@ITQ5AVAT3FYWNWJL"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    while True:
        try:
            bot.send_message(channel_username, "🔥 Free movies yaha milengi 🎬")
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(10)

if __name__ == "__main__":
    # Flask pehle start karo (IMPORTANT)
    port = int(os.environ.get("PORT", 10000))

    # Bot background me
    Thread(target=run_bot).start()

    app.run(host="0.0.0.0", port=port)
