import telebot
import time
import os
from flask import Flask
from threading import Thread

# 1. Naya Token (Render se lega)
token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

# 2. Aapki Sahi Details
database_id = -1003867813389  # Aapki Database ID
target_channel = "@ITQSAVAT3FYVNWUL" # Aapka Main Channel

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 3. Forwarding Logic
def run_bot_logic():
    # Humne 217 set kiya hai kyunki aapki movie wahan se shuru hai
    msg_id = 217 
    print(f"Forwarding started from Message ID: {msg_id}")
    
    while True:
        try:
            bot.forward_message(chat_id=target_channel, from_chat_id=database_id, message_id=msg_id)
            print(f"SUCCESS: Movie {msg_id} forwarded!")
            msg_id += 1
            time.sleep(300) # Har 5 minute mein ek movie
            
        except Exception as e:
            # Agar ID khali hai toh 2 second wait karke agla check karega
            print(f"SKIP/ERROR at ID {msg_id}: {e}")
            msg_id += 1
            time.sleep(2)

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    t = Thread(target=run_server)
    t.start()
    run_bot_logic()
    
