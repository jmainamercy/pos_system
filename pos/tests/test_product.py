from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_list_product(client):
    response = client.get("/products")
    assert response.status_code == 200


def test_create_product(client):
    product_data = {
        "category_id": 1,
        "supplier_id": 5,
        "barcode": "APP2026",
        "name": "apple",
        "price": 20.0,
        "cost_price": 20.0,
        "stock_qty": 2,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
