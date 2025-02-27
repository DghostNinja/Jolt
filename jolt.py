import os
import requests
from bs4 import BeautifulSoup

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Your bot token
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Your chat ID or group ID

MOVIES = ["Solo Leveling", "Legend of Vox Machina", "The Witcher"]  # Edit this list
SEARCH_URL = "https://www.google.com/search?q="  # Google search URL


def search_movie_updates(movie_title):
    """Searches the web for new movie releases."""
    query = f"{movie_title} new season release date"
    url = SEARCH_URL + query.replace(" ", "+")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract relevant data (Modify if needed)
    results = soup.find_all("span")  # Adjust selector
    for result in results:
        if "season" in result.text.lower() or "release" in result.text.lower():
            return result.text.strip()
    return None


def send_telegram_message(message):
    """Sends a notification to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error sending message: {response.text}")


def main():
    for movie in MOVIES:
        update = search_movie_updates(movie)
        if update:
            message = f"📢 Movie Update: {movie}\n{update}"
            send_telegram_message(message)
        else:
            print(f"No new updates for {movie}.")


if __name__ == "__main__":
    main()
