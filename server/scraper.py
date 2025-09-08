import requests
import json
import logging
from datetime import datetime
from pathlib import Path
from utils import setup_logger

logger = setup_logger(__name__)

logger.info("Starting scraping function...")

logging.basicConfig(level=logging.INFO)

DATA_DIR = Path(__file__).parent / "scraped_data"
DATA_DIR.mkdir(exist_ok=True)

def scrape_products(url="http://localhost:5000/products"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        logging.info(f"Fetching {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Handle both JSON structures: dict of products OR list
        if isinstance(data, dict) and "products" in data:
            items = data["products"]  # use value of key "products"
        elif isinstance(data, list):
            items = data  # already a list
        else:
            raise ValueError("Unexpected API response format")

        products = [
            {
                "name": item.get("title", item.get("name", "Untitled")),
                "qty": item.get("qty", 10),
                "price": float(item.get("price", 0.0))
            }
            for item in items
        ]

        # Save file
        filename = DATA_DIR / f"scraped_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4)

        logging.info(f"Scraped products saved to {filename}")
        return products

    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return [{"error": str(e)}]