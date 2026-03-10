import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

urls = {
    "SuperTwins": "https://www.americanflattrack.com/standings/132916/349628",
    "Singles": "https://www.americanflattrack.com/standings/132916/349627"
}

def get_riders(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Target the specific links within the standings table
        names = []
        for link in soup.select('td a[href*="/riders/view/"]'):
            name = link.get_text(strip=True)
            if name and name not in names:
                names.append(name)
        return names if len(names) > 5 else None
    except:
        return None

st = get_riders(urls["SuperTwins"])
si = get_riders(urls["Singles"])

# IMPORTANT: Only save if we actually found names
if st and si:
    data = {
        "last_updated": datetime.now().strftime("%m/%d %I:%M%p"),
        "SuperTwins": st,
        "Singles": si
    }
    with open('riders.json', 'w') as f:
        json.dump(data, f)
    print("Success: Updated riders.json")
else:
    print("Error: Could not find riders. Keeping old file.")
