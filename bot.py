import telebot
import time
import os

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

channel_username = "@ITQ5AVAT3FYWNWJL"

while True:
    try:
        bot.send_message(channel_username, "Hello bhai! Auto message 🚀")
        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(10)
