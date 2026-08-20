import datetime
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = "8963670220:AAGvrNBKdJSblslB_wthGwYhXdL8p7mUKH0"
CHAT_ID = "-1003932990702"
TMDB_API_KEY = "7d2aedfc44e8dacf0fb1ddbf73c3986a"

# ભાષાના શોર્ટ કોડનું પૂરું નામ
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
        "with_original_language": "hi|gu|te|ta|kn|ml",
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
        
        caption = (
            f"🎬 *COMING SOON TO CINEMAS* 🎬\n\n"
            f"🍿 *Movie Name:* {title}\n"
            f"🗣️ *Language:* {language_name}\n"
            f"📅 *Release Date:* {target_date}\n\n"
            f"📌 _Note: This movie will be available on our channel 2 days after theatrical release. Stay tuned!_"
        )
        
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            await bot.send_photo(chat_id=CHAT_ID, photo=poster_url, caption=caption, parse_mode="Markdown")
        else:
            await bot.send_message(chat_id=CHAT_ID, text=caption, parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(auto_fetch_and_post())
    
