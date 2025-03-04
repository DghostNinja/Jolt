import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
print(ASCII_ART)

# Print the current date when script runs
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"📅 Script started on: {current_date}")

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  

MOVIES = [
    "Solo Leveling", "Demon Slayer Infinity Castle", "All American", "Sakamoto Days", 
    "Final Destination: Bloodlines", "Rick and Morty", "Death of a Unicorn", 
    "How to Train Your Dragon 4", "Den of Thieves 2: Pantera", 
    "The Old Guard 2", "The Legend of Vox Machina", "The Witcher"
]
SEARCH_URL = "https://www.google.com/search?q="  

def search_movie_updates(movie_title):
    """Searches the web for new movie releases and episode details."""
    query = f"{movie_title} latest episode title and release date site:imdb.com OR site:rottentomatoes.com"
    url = SEARCH_URL + query.replace(" ", "+")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all(["h3", "span", "div"])  # Searches for different tags
    episodes = []

    for result in results:
        text = result.text.strip().lower()
        if "episode" in text or "season" in text or "release" in text:
            episodes.append(result.text.strip())

    return "\n".join(episodes) if episodes else None

def send_telegram_message(message):
    """Sends a notification to Telegram and provides debug output."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()

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
            message = f"📢 Movie Update ({current_date}):\n🎬 *{movie}*\n{update}"
        else:
            message = f"ℹ️ No new updates for *{movie}* as of {current_date}."

        send_telegram_message(message)

if __name__ == "__main__":
    main()
