import os
import datetime
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("8963670220:AAGvrNBKdJSblslB_wthGwYhXdL8p7mUKH0")
CHAT_ID = os.getenv("-1003932990702")
TMDB_API_KEY = os.getenv("7d2aedfc44e8dacf0fb1ddbf73c3986a")

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
    
    for movie in movies:
        title = movie.get("title")
        poster_path = movie.get("poster_path")
        orig_lang = movie.get("original_language", "").upper()
        
        caption = (
            f"🔥 **COMING SOON** 🔥\n\n"
            f"🎬 **Movie:** {title}\n"
            f"🗣️ **Language:** {orig_lang}\n"
            f"📅 **Release Date:** {target_date}\n\n"
            f"📝 *Note: આ મૂવી 2 દિવસ પછી આપણી ચેનલમાં ઉપલબ્ધ થશે.*"
        )
        
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/original{poster_path}"
            await bot.send_photo(chat_id=CHAT_ID, photo=poster_url, caption=caption, parse_mode="Markdown")
        else:
            await bot.send_message(chat_id=CHAT_ID, text=caption, parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(auto_fetch_and_post())
    
