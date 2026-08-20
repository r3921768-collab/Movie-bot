import os
import json
import datetime
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = "8963670220:AAGvrNBKdJSblslB_wthGwYhXdL8p7mUKH0"
CHAT_ID = "-1003932990702"
TMDB_API_KEY = "7d2aedfc44e8dacf0fb1ddbf73c3986a"
HISTORY_FILE = "posted_messages.json"

# કેટલા દિવસ પછી પોસ્ટ ડિલીટ કરવી (અહીં 2 દિવસ રાખ્યા છે)
DELETE_AFTER_DAYS = 2

LANG_MAP = {
    "hi": "Hindi",
    "gu": "Gujarati",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam"
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

async def cleanup_old_posts(bot: Bot, history: list):
    """જૂના (2 દિવસ જૂના) મેસેજ ડિલીટ કરશે"""
    now = datetime.datetime.now()
    remaining_history = []
    
    for item in history:
        post_time = datetime.datetime.fromisoformat(item["timestamp"])
        msg_id = item["message_id"]
        
        # જો મેસેજ 2 દિવસ જૂનો થઈ ગયો હોય તો ડિલીટ કરો
        if (now - post_time).days >= DELETE_AFTER_DAYS:
            try:
                await bot.delete_message(chat_id=CHAT_ID, message_id=msg_id)
                print(f"Deleted old message: {msg_id}")
            except Exception as e:
                print(f"Could not delete message {msg_id}: {e}")
        else:
            remaining_history.append(item)
            
    return remaining_history

async def auto_fetch_and_post():
    bot = Bot(token=BOT_TOKEN)
    history = load_history()
    
    # 1. પહેલા જૂના મેસેજ ડિલીટ કરો
    history = await cleanup_old_posts(bot, history)
    
    today = datetime.date.today()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    
    # 2. નવી મુવી શોધો
    movie_url = "https://api.themoviedb.org/3/discover/movie"
    movie_params = {
        "api_key": TMDB_API_KEY,
        "primary_release_date.gte": start_date,
        "primary_release_date.lte": end_date,
        "with_original_language": "hi|gu|te|ta|kn|ml",
        "region": "IN",
        "sort_by": "popularity.desc"
    }
    
    movie_response = requests.get(movie_url, params=movie_params).json()
    movies = movie_response.get("results", [])
    
    for movie in movies[:1]:
        title = movie.get("title")
        poster_path = movie.get("poster_path")
        release_date = movie.get("release_date", "Coming Soon")
        orig_lang = movie.get("original_language", "")
        language_name = LANG_MAP.get(orig_lang, "Indian Regional")
        rating = movie.get("vote_average", "N/A")
        
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            caption = (
                f"🎬 *{title.upper()}*\n\n"
                f"┌ 🏷️ *Type:* Indian Movie\n"
                f"├ 🗣️ *Language:* {language_name}\n"
                f"├ 📅 *Release Date:* {release_date}\n"
                f"└ ⭐ *Rating:* {rating}/10\n\n"
                f"📌 _Note: This movie will be available on our channel soon. Stay tuned!_"
            )
            sent_msg = await bot.send_photo(chat_id=CHAT_ID, photo=poster_url, caption=caption, parse_mode="Markdown")
            
            # મેસેજની ID સેવ કરો જેથી ભવિષ્યમાં ડિલીટ કરી શકાય
            history.append({
                "message_id": sent_msg.message_id,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
    save_history(history)

if __name__ == "__main__":
    asyncio.run(auto_fetch_and_post())
    
