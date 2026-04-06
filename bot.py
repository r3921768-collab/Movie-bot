import telebot
import time
import os
from flask import Flask
from threading import Thread

# 1. Token setup
token = os.getenv("BOT_TOKEN")
if not token:
    raise Exception("BOT_TOKEN missing!")

bot = telebot.TeleBot(token)

# 2. Channel Settings
database_id = -100123515592  # Aapki Database ID
channel_username = "@ITQSAVAT3FYVNWUL" # Aapka Main Channel

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running and live!"

# 3. Yeh function movie forward karega
def run_bot_logic():
    # msg_id ko wahan se shuru karein jahan movie hai (e.g. 100)
    # Agar 1 se shuru karenge toh bot 1, 2, 3 check karega jab tak movie na mile
    msg_id = 1 
    print("Forwarding logic started...")
    
    while True:
        try:
            # Movie forward karne ki koshish
            bot.forward_message(chat_id=channel_username, from_chat_id=database_id, message_id=msg_id)
            print(f"SUCCESS: Message {msg_id} forwarded!")
            msg_id += 1
            time.sleep(300) # Har 5 minute mein ek post
            
        except Exception as e:
            # Agar ID nahi mili (khali message), toh agle ID par jao
            print(f"SKIP ID {msg_id}: {e}")
            msg_id += 1
            time.sleep(2) # 2 second wait karke agla check karein

# 4. Flask ko background mein chalane ke liye
def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Pehle Flask (Server) ko alag thread mein start karein
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
    
    # Fir Bot ki logic chalu karein
    run_bot_logic()
    
