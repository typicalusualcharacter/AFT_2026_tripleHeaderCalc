import requests
from bs4 import BeautifulSoup
import json

urls = {
    "SuperTwins": "https://www.americanflattrack.com/standings/132916/349628",
    "Singles": "https://www.americanflattrack.com/standings/132916/349627"
}

def get_riders(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # This finds the names in the AFT standings table
        cells = soup.find_all('td', class_='rider')
        names = sorted(list(set([c.get_text(strip=True) for c in cells if c.get_text(strip=True)])))
        return names if names else ["Error: No names found"]
    except Exception as e:
        return [f"Error: {str(e)}"]

data = {
    "SuperTwins": get_riders(urls["SuperTwins"]),
    "Singles": get_riders(urls["Singles"])
}

with open('riders.json', 'w') as f:
    json.dump(data, f)
