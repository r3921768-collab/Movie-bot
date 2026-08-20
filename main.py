import datetime
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = "8963670220:AAGvrNBKdJSblslB_wthGwYhXdL8p7mUKH0"
CHAT_ID = "-1003932990702"
TMDB_API_KEY = "7d2aedfc44e8dacf0fb1ddbf73c3986a"

LANG_MAP = {
    "hi": "Hindi",
    "gu": "Gujarati",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam"
}

async def auto_fetch_and_post():
    bot = Bot(token=BOT_TOKEN)
    
    today = datetime.date.today()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    
    # અહિંયા ભાષા અને પ્રદેશ સેટ કરેલા છે જેથી હોલીવુડ ફિલ્મો નહીં આવે
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "primary_release_date.gte": start_date,
        "primary_release_date.lte": end_date,
        "with_original_language": "hi|gu|te|ta|kn|ml",
        "region": "IN",
        "sort_by": "popularity.desc"
    }
    
    response = requests.get(url, params=params).json()
    movies = response.get("results", [])
    
    # માત્ર ૧ જ મૂવી મોકલશે
    MAX_POSTS = 1
    count = 0
    
    for movie in movies:
        if count >= MAX_POSTS:
            break
            
        title = movie.get("title")
        poster_path = movie.get("poster_path")
        release_date = movie.get("release_date", "Coming Soon")
        orig_lang = movie.get("original_language", "")
        language_name = LANG_MAP.get(orig_lang, "Indian Regional")
        rating = movie.get("vote_average", "N/A")
        
        if not poster_path:
            continue
            
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        
        caption = (
            f"🎬 *{title.upper()}*\n\n"
            f"┌ 🏷️ *Type:* Indian Movie\n"
            f"├ 🗣️ *Language:* {language_name}\n"
            f"├ 📅 *Release Date:* {release_date}\n"
            f"└ ⭐ *Rating:* {rating}/10\n\n"
            f"📌 _Note: This movie will be available on our channel soon. Stay tuned!_"
        )
        
        await bot.send_photo(chat_id=CHAT_ID, photo=poster_url, caption=caption, parse_mode="Markdown")
        count += 1

if __name__ == "__main__":
    asyncio.run(auto_fetch_and_post())
    
