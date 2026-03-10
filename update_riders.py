import requests
from bs4 import BeautifulSoup
import json

# The links you provided
urls = {
    "SuperTwins": "https://www.americanflattrack.com/standings/132916/349628",
    "Singles": "https://www.americanflattrack.com/standings/132916/349627"
}

def get_riders(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all table cells that contain rider names
    # Note: AFT's site structure may require minor tweaks to this selector
    rider_tags = soup.find_all('td', class_='rider') 
    names = [t.get_text(strip=True) for t in rider_tags]
    return names if names else ["Rider List Error"]

data = {
    "SuperTwins": get_riders(urls["SuperTwins"]),
    "Singles": get_riders(urls["Singles"])
}

with open('riders.json', 'w') as f:
    json.dump(data, f)
