import os
import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name__)

# ASCII Art
ASCII_ART = r"""
    ___  ________  ___   _________           
   |\  \|\   __  \|\  \ |\___   ___\         
   \ \  \ \  \|\  \ \  \\|___ \  \_|         
 __ \ \  \ \  \\\  \ \  \    \ \  \          
|\  \\_\  \ \  \\\  \ \  \____\ \  \         
\ \________\ \_______\ \_______\ \__\        
 \|________|\|_______|\|_______|\|__|        
                                             
                                             by iPsalmy
"""

print(ASCII_ART)  # Display ASCII art at script start

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

MOVIE_LIST_FILE = "movies.json"  # JSON file to store movies

# Load movies from file
def load_movies():
    if os.path.exists(MOVIE_LIST_FILE):
        with open(MOVIE_LIST_FILE, "r") as file:
            return json.load(file)
    return []

# Save movies to file
def save_movies(movies):
    with open(MOVIE_LIST_FILE, "w") as file:
        json.dump(movies, file)

# Function to handle incoming Telegram messages
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def receive_message():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].strip()
        
        if text.lower() == "/list":
            movies = load_movies()
            message = "🎬 Your movie list:\n" + "\n".join(movies) if movies else "📭 No movies added yet."
        
        elif text.lower().startswith("/add"):
            movie_name = text[5:].strip()
            if movie_name:
                movies = load_movies()
                movies.append(movie_name)
                save_movies(movies)
                message = f"✅ '{movie_name}' added to your watchlist!"
            else:
                message = "⚠️ Please provide a movie name after /add"

        elif text.lower().startswith("/remove"):
            movie_name = text[8:].strip()
            movies = load_movies()
            if movie_name in movies:
                movies.remove(movie_name)
                save_movies(movies)
                message = f"❌ '{movie_name}' removed from your watchlist!"
            else:
                message = "⚠️ Movie not found in list."

        else:
            message = "🤖 Commands:\n/add <movie>\n/remove <movie>\n/list"

        send_telegram_message(chat_id, message)

    return "OK", 200

# Search for movie updates
def search_movie_updates(movie_title):
    query = f"{movie_title} latest episode release date and title"
    url = f"https://www.google.com/search?q=" + query.replace(" ", "+")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all("span")
    episodes = [result.text.strip() for result in results if "episode" in result.text.lower()]

    return "\n".join(episodes) if episodes else None

# Send a Telegram message
def send_telegram_message(chat_id, message):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, json=payload)

# Main function to check updates
def main():
    movies = load_movies()
    if not movies:
        return

    for movie in movies:
        update = search_movie_updates(movie)
        message = f"🎬 *{movie}* Update:\n{update}" if update else f"ℹ️ No new updates for {movie}."
        send_telegram_message(TELEGRAM_CHAT_ID, message)

if __name__ == "__main__":
    app.run(port=5000)
