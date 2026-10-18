import asyncio
import datetime
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from telegram import Bot

BOT_TOKEN = "8963670220:AAGvrNBKdJSbls1B_wthGwYhXdL8p7mUKH0"
CHAT_ID = "-1003932990702"
SECOND_CHANNEL_ID = "-1003393813099"  # 👈 Tamari biji channel ni ID ahiya muko
TMDB_API_KEY = "7d2aedfc44e8dacf0fb1ddbf73..."
HISTORY_FILE = "posted_messages.json"

DELETE_AFTER_DAYS = 2

LANG_MAP = {
    "hi": "Hindi",
    "gu": "Gujarati",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
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


async def auto_fetch_and_post():
  bot = Bot(token=BOT_TOKEN)
  history = load_history()

  today = datetime.date.today()
  start_date = today.strftime("%Y-%m-%d")
  end_date = (today + datetime.timedelta(days=14)).strftime("%Y-%m-%d")

  movie_url = "https://api.themoviedb.org/3/discover/movie"
  movie_params = {
      "api_key": TMDB_API_KEY,
      "primary_release_date.gte": start_date,
      "primary_release_date.lte": end_date,
      "with_original_language": "hi|gu|te|ta|kn|ml",
      "region": "IN",
      "sort_by": "popularity.desc",
  }

  response = requests.get(movie_url, params=movie_params)
  movies = response.json().get("results", [])

  for movie in movies:
    title = movie.get("title")
    poster_path = movie.get("poster_path")
    release_date = movie.get("release_date", "Coming Soon")
    orig_lang = movie.get("original_language", "")
    lang_name = LANG_MAP.get(orig_lang, "Indian Regional")
    rating = movie.get("vote_average", "N/A")

    if poster_path:
      poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
      caption = (
          f"🎬 **{title.upper()}**\n\n"
          f"📌 **Type:** Indian Movie\n"
          f"🌐 **Language:** {lang_name}\n"
          f"📅 **Release Date:** {release_date}\n"
          f"⭐ **Rating:** {rating}/10\n\n"
          f"📝 **Note:** This movie will be available on our channel"
      )

            try:
        # 1. Main channel (Database channel) ma permanent photo moklo
        sent_msg_main = await bot.send_photo(
            chat_id=CHAT_ID, photo=poster_url, caption=caption
        )

        # 2. Biji channel ma notice sathe photo moklo
        caption_with_note = (
            caption
            + "\n\n⚠️ **Notice:** This file/message will be automatically deleted"
            " within 5 minutes. Please save or forward it accordingly."
        )
        sent_msg_second = await bot.send_photo(
            chat_id=SECOND_CHANNEL_ID,
            photo=poster_url,
            caption=caption_with_note,
        )

        # 3. 5 minute pachi fkt biji channel valo message delete karva mate task
        async def delete_second_message():
          await asyncio.sleep(300)  # 300 seconds = 5 minutes
          try:
            await sent_msg_second.delete()
          except Exception as e:
            print("Delete error:", e)

        asyncio.create_task(delete_second_message())

        history.append({
            "message_id": sent_msg_main.message_id,
            "timestamp": datetime.datetime.now().isoformat(),
        })
      except Exception as e:
        print("Send error:", e)
          
        history.append({
            "message_id": sent_msg.message_id,
            "timestamp": datetime.datetime.now().isoformat(),
        })
      except Exception as e:
        print("Send error:", e)

  save_history(history)


# Render mate dummy web server jethi app bandh na thay
class SimpleHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is active and running!")


def run_server():
  port = int(os.environ.get("PORT", 10000))
  server = HTTPServer(("0.0.0.0", port), SimpleHandler)
  server.serve_forever()


if __name__ == "__main__":
  # 1. Server ne background ma start karo
  threading.Thread(target=run_server, daemon=True).start()

  # 2. Dar 3 kalake auto-poster run thase
  while True:
    try:
      asyncio.run(auto_fetch_and_post())
    except Exception as e:
      print("Loop error:", e)

    print("Waiting for next run...")
    time.sleep(10800)  # 3 hours = 10800 seconds
        
