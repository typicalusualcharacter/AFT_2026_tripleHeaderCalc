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
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Target only the cells within the table body to avoid headers
        table = soup.find('table')
        if not table: return None
        
        tbody = table.find('tbody')
        cells = tbody.find_all('td', class_=['rider', 'rider-name', 'views-field-field-rider-name']) if tbody else []
        
        names = []
        for cell in cells:
            name = cell.get_text(strip=True)
            # Filter out known header text or empty strings
            if name and name.lower() != "rider(s)" and name not in names:
                names.append(name)
        
        return names if names else None
    except Exception as e:
        print(f"Error: {e}")
        return None

data = {
    "last_updated": datetime.now().strftime("%m/%d/%Y %I:%M %p"),
    "SuperTwins": get_riders(urls["SuperTwins"]),
    "Singles": get_riders(urls["Singles"])
}

with open('riders.json', 'w') as f:
    json.dump(data, f)
