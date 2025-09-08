import pytest
from server.app import app , repo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    repo.DB_PATH = ":memory:"
    repo.product_table_create()
    with app.test_client() as client:
        yield client

def test_create_product_api(client):
    response = client.post("/products", json={"name": "APIProduct", "qty": 3, "price": 50})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == "APIProduct"

def test_list_products_api(client):
    client.post("/products", json={"name": "P1", "qty": 2, "price": 10})
    r = client.get("/products")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_total_stock_api(client):
    client.post("/products", json={"name": "P1", "qty": 10, "price": 5})
    r = client.get("/stock/total")
    assert r.status_code == 200
    data = r.get_json()
    assert "total_stock" in data