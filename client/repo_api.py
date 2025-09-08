import requests

BASE_URL = "http://localhost:5000"

def create_product(p):
    return requests.post(f"{BASE_URL}/products", json=p).json()

def read_all():
    return requests.get(f"{BASE_URL}/products").json()

def read_by_id(pid):
    return requests.get(f"{BASE_URL}/products/{pid}").json()

def update(p):
    return requests.put(f"{BASE_URL}/products/{p['id']}", json=p).json()

def delete_by_id(pid):
    return requests.delete(f"{BASE_URL}/products/{pid}").json()

def get_total_stock():
    return requests.get(f"{BASE_URL}/stock/total").json()

def scrape_products():
    return requests.get(f"{BASE_URL}/products/scrape").json()