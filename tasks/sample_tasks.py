import time
import requests
from bs4 import BeautifulSoup

def add_numbers(payload):
    result = payload['a'] + payload['b']
    return result

def fetch_market_data(payload):
    url = payload["url"]
    return requests.get(url).json()

def cpu_heavy_task(payload):
    n = payload.get("n", 10000000)
    return sum(i*i for i in range(n))

def scrape_website(payload):
    url = payload["url"]

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No title"

        return {
            "url": url,
            "title": title,
            "length": len(response.text)
        }

    except Exception as e:
        raise Exception(f"Scraping failed: {str(e)}")