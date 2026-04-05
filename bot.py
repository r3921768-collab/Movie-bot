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

# bot thread
Thread(target=run_bot).start()

# IMPORTANT: Render port fix
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
