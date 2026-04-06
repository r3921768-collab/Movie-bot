import telebot
import time
import os
import threading
from flask import Flask
from threading import Thread

# 🔐 Bot token
bot = telebot.TeleBot(os.getenv("BOT_TOKEN").strip())

# 📢 Channels
SOURCE_CHANNEL = -1003867813389   # database channel
TARGET_CHANNEL = "@ITQ5AVAT3FYWNWJL"  # main channel

# 📂 Movie storage
movies = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 🔥 AUTO SAVE (database channel se)
@bot.message_handler(content_types=['video', 'document'])
def save_movie(message):
    try:
        # sirf database channel ka data save kare
        if message.chat.id != SOURCE_CHANNEL:
            return

        if message.video:
            name = message.video.file_name or "movie"
        elif message.document:
            name = message.document.file_name or "movie"
        else:
            return

        name = name.lower()
        movies[name] = message.message_id

        print(f"Saved: {name} -> {message.message_id}")

    except Exception as e:
        print("Save Error:", e)

# 🗑️ Auto delete function
def delete_after(chat_id, msg_id, delay=600):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, msg_id)
    except Exception as e:
        print("Delete Error:", e)

# 🔍 SEARCH SYSTEM
@bot.message_handler(func=lambda message: True)
def search_movie(message):
    try:
        user_text = message.text.lower()

        print("Search:", user_text)
        print("Movies:", movies)

        for name, msg_id in movies.items():
            if user_text in name:
                try:
                    # 🎬 Forward movie
                    sent = bot.forward_message(
                        chat_id=TARGET_CHANNEL,
                        from_chat_id=SOURCE_CHANNEL,
                        message_id=msg_id
                    )

                    # ⚠️ Warning message
                    warn = bot.send_message(
                        TARGET_CHANNEL,
                        "⚠️ Forward fast! Only 10 minutes ⏳\nThis movie will be deleted soon."
                    )

                    # ⏳ Auto delete after 10 min
                    threading.Thread(target=delete_after, args=(TARGET_CHANNEL, sent.message_id)).start()
                    threading.Thread(target=delete_after, args=(TARGET_CHANNEL, warn.message_id)).start()

                    return

                except Exception as e:
                    print("Forward Error:", e)
                    bot.send_message(message.chat.id, "Error sending movie")
                    return

        bot.send_message(message.chat.id, "Movie not available")

    except Exception as e:
        print("Search Error:", e)

# 🤖 Run bot
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
