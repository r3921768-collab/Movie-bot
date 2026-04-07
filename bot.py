import telebot
import os
import time
import threading
from flask import Flask
from threading import Thread

bot = telebot.TeleBot(os.getenv("BOT_TOKEN").strip())

# Channels
SOURCE_CHANNEL = -1003867813389
TARGET_CHANNEL = "@ITQ5AVAT3FYWNWJL"

# Movie mapping
movies = {
    "kgf": 213,
    "pushpa": 214,
    "rrr": 215
}

# User cooldown storage
user_time = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 🗑️ Delete function
def delete_after(chat_id, msg_id, delay=600):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, msg_id)
    except:
        pass

# 🔍 SEARCH + CONTROL
@bot.message_handler(func=lambda message: True)
def search_movie(message):
    user_id = message.from_user.id
    user_text = message.text.lower()

    # ⏱️ Cooldown check (5 min)
    if user_id in user_time:
        diff = time.time() - user_time[user_id]
        if diff < 300:
            bot.send_message(message.chat.id, "⏳ Wait 5 minutes before next request")
            return

    # 🎬 Movie search
    if user_text in movies:
        try:
            # Save user request time
            user_time[user_id] = time.time()

            # Forward movie to main channel
            sent = bot.forward_message(
                chat_id=TARGET_CHANNEL,
                from_chat_id=SOURCE_CHANNEL,
                message_id=movies[user_text]
            )

            # Warning message
            warn = bot.send_message(
                TARGET_CHANNEL,
                "⚠️ Forward fast! Only 10 minutes ⏳\nThis movie will be deleted soon."
            )

            # Auto delete after 10 min
            threading.Thread(target=delete_after, args=(TARGET_CHANNEL, sent.message_id)).start()
            threading.Thread(target=delete_after, args=(TARGET_CHANNEL, warn.message_id)).start()

        except Exception as e:
            print("Error:", e)
            bot.send_message(message.chat.id, "⚠️ Error sending movie")

    else:
        bot.send_message(message.chat.id, "❌ Movie not available")

# Run bot
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
