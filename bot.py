import telebot
import os
import time
import threading
from flask import Flask
from threading import Thread

# 🔐 Bot token
bot = telebot.TeleBot(os.getenv("BOT_TOKEN").strip())

# 📢 Channels
SOURCE_CHANNEL = -1003867813389   # database channel
TARGET_CHANNEL = "@ITQ5AVAT3FYWNWJL"  # main channel

# 🎬 Movie mapping (yaha apni movies add kar)
movies = {
    "kgf": 213,
    "pushpa": 214,
    "rrr": 215
}

# ⏱️ Cooldown system
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

# 🔍 MAIN HANDLER
@bot.message_handler(func=lambda message: message.text is not None)
def search_movie(message):
    user_id = message.from_user.id
    user_text = message.text.lower().strip()

    # ❌ ignore unwanted messages (only words allowed)
    if len(user_text) < 2:
        return

    # ⏱️ Cooldown check (5 min)
    if user_id in user_time:
        diff = time.time() - user_time[user_id]
        if diff < 300:
            bot.send_message(message.chat.id, "⏳ Wait 5 minutes before next request")
            return

    # 🎬 Search movie
    if user_text in movies:
        try:
            user_time[user_id] = time.time()

            # 🎬 Forward movie
            sent = bot.forward_message(
                chat_id=TARGET_CHANNEL,
                from_chat_id=SOURCE_CHANNEL,
                message_id=movies[user_text]
            )

            # ⚠️ Warning message
            warn = bot.send_message(
                TARGET_CHANNEL,
                "⚠️ Forward fast! Only 10 minutes ⏳\nThis movie will be deleted soon."
            )

            # 🗑️ Auto delete after 10 min
            threading.Thread(target=delete_after, args=(TARGET_CHANNEL, sent.message_id)).start()
            threading.Thread(target=delete_after, args=(TARGET_CHANNEL, warn.message_id)).start()

        except Exception as e:
            print("Error:", e)
            bot.send_message(message.chat.id, "⚠️ Error sending movie")

    else:
        # ❌ Movie not found (only if proper word)
        if user_text.isalpha():
            bot.send_message(message.chat.id, "❌ Movie not available")

# 🤖 Run bot
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
