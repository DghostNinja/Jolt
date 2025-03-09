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

SEARCH_URLS = {
    "Google": "https://www.google.com/search?q=",
    "Nkiri": "https://nkiri.com/?s=",
    "O2TvSeries": "https://o2tvseries.com/search/?q=",
    "AnimePahe": "https://animepahe.ru/search?q="
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def search_movie_updates(movie_title):
    """Searches Google, Nkiri, O2TvSeries, and AnimePahe for new episodes."""
    results = []

    # Google Search
    google_query = f"{movie_title} latest episode title and release date site:imdb.com OR site:rottentomatoes.com OR site:netflix.com"
    google_url = SEARCH_URLS["Google"] + google_query.replace(" ", "+")
    google_response = requests.get(google_url, headers=HEADERS)
    google_soup = BeautifulSoup(google_response.text, "html.parser")

    for tag in google_soup.find_all(["h3", "span", "div"]):
        text = tag.text.strip()
        if "episode" in text.lower() or "season" in text.lower() or "release" in text.lower():
            results.append(text)

    # Nkiri Search
    nkiri_url = SEARCH_URLS["Nkiri"] + movie_title.replace(" ", "+")
    nkiri_response = requests.get(nkiri_url, headers=HEADERS)
    nkiri_soup = BeautifulSoup(nkiri_response.text, "html.parser")
    for link in nkiri_soup.find_all("a", href=True):
        if "episode" in link.text.lower() or "season" in link.text.lower():
            results.append(f"Nkiri: {link.text.strip()} ➡ {link['href']}")

    # O2TvSeries Search
    o2tv_url = SEARCH_URLS["O2TvSeries"] + movie_title.replace(" ", "+")
    o2tv_response = requests.get(o2tv_url, headers=HEADERS)
    o2tv_soup = BeautifulSoup(o2tv_response.text, "html.parser")
    for link in o2tv_soup.find_all("a", href=True):
        if "episode" in link.text.lower() or "season" in link.text.lower():
            results.append(f"O2TvSeries: {link.text.strip()} ➡ {link['href']}")

    # AnimePahe Search
    animepahe_url = SEARCH_URLS["AnimePahe"] + movie_title.replace(" ", "+")
    animepahe_response = requests.get(animepahe_url, headers=HEADERS)
    animepahe_soup = BeautifulSoup(animepahe_response.text, "html.parser")
    for link in animepahe_soup.find_all("a", href=True):
        if "episode" in link.text.lower() or "season" in link.text.lower():
            results.append(f"AnimePahe: {link.text.strip()} ➡ {link['href']}")

    return "\n".join(results) if results else None

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
