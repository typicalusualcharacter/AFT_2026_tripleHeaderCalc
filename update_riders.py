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
        
        # AFT Standings tables use <td> with class "rider" or "rider-name"
        # We find all cells that are likely to contain names
        cells = soup.find_all('td', class_=['rider', 'rider-name', 'views-field-field-rider-name'])
        
        names = []
        for cell in cells:
            name = cell.get_text(strip=True)
            if name and name not in names:
                names.append(name)
        
        # If the above fails, try a broader search for table rows
        if not names:
            rows = soup.find_all('tr')
            for row in rows:
                # Typically the rider name is in the second or third column
                cols = row.find_all('td')
                if len(cols) > 1:
                    name = cols[1].get_text(strip=True) # Usually index 1 or 2
                    if name and not name.isdigit() and len(name) > 3:
                        names.append(name)

        return names if names else None
    except Exception as e:
        print(f"Error: {e}")
        return None

st_names = get_riders(urls["SuperTwins"])
si_names = get_riders(urls["Singles"])

data = {
    "last_updated": datetime.now().strftime("%m/%d/%Y %I:%M %p"),
    "SuperTwins": st_names,
    "Singles": si_names
}

with open('riders.json', 'w') as f:
    json.dump(data, f)
