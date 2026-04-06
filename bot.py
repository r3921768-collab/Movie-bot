import telebot
import time
import os
from flask import Flask
from threading import Thread

# 1. Token setup (Render ke Environment Variables se lega)
token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

# 2. Sahi ID jo aapne nikaali hai
database_id = -1003867813389  # Aapki Database ID
target_channel = "@ITQSAVAT3FYVNWUL" # Aapka Main Channel

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 3. Movie Forward karne ki logic
def run_bot_logic():
    # msg_id = 1 se shuru karein taaki bot pehli post se check kare
    msg_id = 1 
    print(f"Forwarding started from: {database_id}")
    
    while True:
        try:
            # Ye command movie forward karegi
            bot.forward_message(chat_id=target_channel, from_chat_id=database_id, message_id=msg_id)
            print(f"SUCCESS: Message {msg_id} forwarded!")
            
            msg_id += 1
            time.sleep(300) # Har 5 minute mein ek movie (Aap ise badal sakte hain)
            
        except Exception as e:
            # Agar ID khali hai toh 2 second baad agla check karega
            print(f"SKIP ID {msg_id}: {e}")
            msg_id += 1
            time.sleep(2)

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask start karein
    t = Thread(target=run_server)
    t.start()
    
    # Forwarding logic start karein
    run_bot_logic()
    
    
