import telebot
import time
import os
from flask import Flask
from threading import Thread

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# Database channel ID
SOURCE_CHANNEL = -1003867813389

# Temporary movie storage
movies = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 🔥 AUTO INDEX (jab bhi movie upload hogi database me)
@bot.channel_post_handler(content_types=['video', 'document'])
def save_movie(message):
    try:
        file_name = ""

        if message.video:
            file_name = message.video.file_name or "unknown"

        elif message.document:
            file_name = message.document.file_name or "unknown"

        file_name = file_name.lower()

        movies[file_name] = message.message_id

        print(f"Saved: {file_name} -> {message.message_id}")

    except Exception as e:
        print("Index Error:", e)

# 🔍 AUTO SEARCH SYSTEM
@bot.message_handler(func=lambda message: True)
def search_movie(message):
    user_text = message.text.lower()

    for name, msg_id in movies.items():
        if user_text in name:
            try:
                bot.forward_message(
                    chat_id=message.chat.id,
                    from_chat_id=SOURCE_CHANNEL,
                    message_id=msg_id
                )
                return
            except Exception as e:
                print("Forward Error:", e)
                bot.send_message(message.chat.id, "⚠️ Error sending movie")

    bot.send_message(message.chat.id, "❌ Movie not available")

# Bot run
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
