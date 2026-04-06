import telebot
import time
import os
import threading
from flask import Flask
from threading import Thread

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# 🔥 Channels
SOURCE_CHANNEL = -1003867813389  # database channel ID
TARGET_CHANNEL = "@ITQ5AVAT3FYWNWJL"  # main channel

# 📂 Temporary storage
movies = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 🔥 AUTO INDEX (save movies from database)
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

# 🗑️ DELETE FUNCTION
def delete_after(chat_id, msg_id, delay=600):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, msg_id)
    except Exception as e:
        print("Delete Error:", e)

# 🔍 SEARCH + SEND
@bot.message_handler(func=lambda message: True)
def search_movie(message):
    user_text = message.text.lower()

    for name, msg_id in movies.items():
        if user_text in name:
            try:
                # 🎬 Movie forward
                sent_movie = bot.forward_message(
                    chat_id=TARGET_CHANNEL,
                    from_chat_id=SOURCE_CHANNEL,
                    message_id=msg_id
                )

                # ⚠️ Warning message
                warning = bot.send_message(
                    TARGET_CHANNEL,
                    "⚠️ Forward fast! Only 10 minutes ⏳\nThis movie will be deleted soon."
                )

                # ⏳ Auto delete after 10 min
                threading.Thread(target=delete_after, args=(TARGET_CHANNEL, sent_movie.message_id)).start()
                threading.Thread(target=delete_after, args=(TARGET_CHANNEL, warning.message_id)).start()

                return

            except Exception as e:
                print("Error:", e)
                bot.send_message(message.chat.id, "⚠️ Error sending movie")

    bot.send_message(message.chat.id, "❌ Movie not available")

# 🤖 RUN BOT
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
