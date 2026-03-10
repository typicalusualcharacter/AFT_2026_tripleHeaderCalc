import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# The links for 2026 standings
urls = {
    "SuperTwins": "https://www.americanflattrack.com/standings/132916/349628",
    "Singles": "https://www.americanflattrack.com/standings/132916/349627"
}

def get_riders(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # AFT 2026 specific: Look for links inside table rows that contain the rider profile
        rider_links = soup.find_all('a', href=lambda href: href and '/riders/view/' in href)
        names = []
        for link in rider_links:
            name = link.get_text(strip=True)
            if name and name not in names:
                names.append(name)
        
        return sorted(names) if names else None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Attempt to pull new data
st_names = get_riders(urls["SuperTwins"])
si_names = get_riders(urls["Singles"])

# Final data structure
data = {
    "last_updated": datetime.now().strftime("%m/%d/%Y %I:%M %p"),
    "SuperTwins": st_names,
    "Singles": si_names
}

with open('riders.json', 'w') as f:
    json.dump(data, f)
