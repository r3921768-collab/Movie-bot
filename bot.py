import telebot
import time
import os
from flask import Flask
from threading import Thread

token = os.getenv("BOT_TOKEN")

if not token:
    raise Exception("BOT_TOKEN missing!")

bot = telebot.TeleBot(token)
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
            print("BOT ERROR:", e)
            time.sleep(10)

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 10000))
        Thread(target=run_bot).start()
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        print("MAIN ERROR:", e)
