import telebot
import os
from flask import Flask
from threading import Thread

bot = telebot.TeleBot(os.getenv("BOT_TOKEN").strip())

# Channels
SOURCE_CHANNEL = -1003867813389
TARGET_CHANNEL = "@ITQ5AVAT3FYWNWJL"

# Movies (correct ID daal)
movies = {
    "kgf": 213,
    "pushpa": 214
}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(func=lambda message: True)
def send_movie(message):
    text = message.text.lower().strip()

    if text in movies:
        try:
            bot.forward_message(
                chat_id=TARGET_CHANNEL,
                from_chat_id=SOURCE_CHANNEL,
                message_id=movies[text]
            )
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "⚠️ Movie send error")
    else:
        bot.send_message(message.chat.id, "please wait...🙏🎥")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
