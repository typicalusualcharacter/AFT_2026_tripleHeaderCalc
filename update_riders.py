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
        
        # The 2026 standings use a table with a specific structure
        # We find the table, then look for rows, then the rider column
        names = []
        rows = soup.find_all('tr')
        
        for row in rows:
            # Look for the 'rider' or 'rider-name' class in the cell
            rider_cell = row.find('td', class_=['rider', 'rider-name', 'views-field-field-rider-name'])
            if rider_cell:
                # Get the link text (the name)
                link = rider_cell.find('a')
                name = link.get_text(strip=True) if link else rider_cell.get_text(strip=True)
                
                if name and name.lower() != "rider(s)" and name not in names:
                    names.append(name)
        
        print(f"Found {len(names)} riders for {url}")
        return names if names else None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Execute
st_list = get_riders(urls["SuperTwins"])
si_list = get_riders(urls["Singles"])

data = {
    "last_updated": datetime.now().strftime("%m/%d/%Y %I:%M %p"),
    "SuperTwins": st_list,
    "Singles": si_list
}

with open('riders.json', 'w') as f:
    json.dump(data, f)
