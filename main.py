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
    "ml": "Malayalam",
    "en": "English"
}

async def auto_fetch_and_post():
    bot = Bot(token=BOT_TOKEN)
    
    # 2 દિવસ પછીની તારીખ
    target_date = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "primary_release_date.gte": target_date,
        "primary_release_date.lte": target_date,
        "region": "IN",
        "sort_by": "popularity.desc"
    }
    
    response = requests.get(url, params=params).json()
    movies = response.get("results", [])
    
    if not movies:
        print("No movies found for this date.")
        return

    for movie in movies:
        title = movie.get("title")
        poster_path = movie.get("poster_path")
        orig_lang = movie.get("original_language", "")
        language_name = LANG_MAP.get(orig_lang, orig_lang.upper())
        overview = movie.get("overview", "")
        rating = movie.get("vote_average", "N/A")
        
        # જો પોસ્ટર ન હોય તો મેસેજ સ્કીપ કરવો
        if not poster_path:
            continue
            
        poster_url = f"https://image.tmdb.org/t/p/original{poster_path}"
        
        caption = (
            f"🎬 **{title.upper()}**\n\n"
            f"┌ 🏷️ **Type:** Movie\n"
            f"├ 🗣️ **Language:** {language_name}\n"
            f"├ 📅 **Release Date:** {target_date}\n"
            f"└ ⭐ **Rating:** {rating}/10\n\n"
            f"📌 **Note:** *This movie will be uploaded to our channel 2 days after release. Stay tuned!*"
        )
        
        await bot.send_photo(chat_id=CHAT_ID, photo=poster_url, caption=caption, parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(auto_fetch_and_post())
    
    
