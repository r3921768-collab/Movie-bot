import telebot
import os
from flask import Flask
from threading import Thread

# 🔐 Bot token
bot = telebot.TeleBot(os.getenv("BOT_TOKEN").strip())

# 📢 Channels
SOURCE_CHANNEL = -1003867813389   # database
TARGET_CHANNEL = "@ITQ5AVAT3FYWNWJL"  # main channel

# 🎬 Movies (apni ID yaha daal)
movies = {
    "kgf": 213,
    "pushpa": 214,
    "rrr": 215
}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 🔍 SEARCH SYSTEM
@bot.message_handler(func=lambda message: message.text is not None)
def search_movie(message):
    user_text = message.text.lower().strip()

    if user_text in movies:
        try:
            bot.forward_message(
                chat_id=TARGET_CHANNEL,
                from_chat_id=SOURCE_CHANNEL,
                message_id=movies[user_text]
            )
        except Exception as e:
            print("Error:", e)
            bot.send_message(message.chat.id, "⚠️ Error sending movie")
    else:
        bot.send_message(message.chat.id, "❌ Movie not available")

# 🤖 Run bot
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
