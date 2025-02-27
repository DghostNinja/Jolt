import os
import requests
from bs4 import BeautifulSoup

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
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Your bot token
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Your chat ID or group ID

MOVIES = ["Solo Leveling", "Legend of Vox Machina", "The Witcher"]  # Edit this list
SEARCH_URL = "https://www.google.com/search?q="  # Google search URL


def search_movie_updates(movie_title):
    """Searches the web for new movie releases and episode details."""
    query = f"{movie_title} latest episode release date and title"
    url = SEARCH_URL + query.replace(" ", "+")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract possible episode details
    results = soup.find_all("span")  # Adjust selector if needed
    episodes = []

    for result in results:
        text = result.text.strip().lower()
        if "episode" in text or "season" in text or "release" in text:
            episodes.append(result.text.strip())

    if episodes:
        return "\n".join(episodes)
    
    return None


def send_telegram_message(message):
    """Sends a notification to Telegram and provides debug output."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()  # Get API response as JSON

        if response.status_code == 200 and response_data.get("ok"):
            print(f"✅ Message sent successfully: {message}")
        else:
            print(f"❌ Failed to send message. Status Code: {response.status_code}")
            print(f"Response: {response_data}")

    except Exception as e:
        print(f"⚠️ Error while sending Telegram message: {e}")


def main():
    for movie in MOVIES:
        update = search_movie_updates(movie)
        if update:
            message = f"📢 Movie Update: {movie}\nLatest Episodes:\n{update}"
        else:
            message = f"ℹ️ No new updates for {movie} yet."

        send_telegram_message(message)


if __name__ == "__main__":
    main()
