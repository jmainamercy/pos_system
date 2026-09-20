def test_product_crud_and_validation(client):
    # list
    r = client.get('/products')
    assert r.status_code == 200

    # create valid product (uses seeded category id=1 and supplier id=5)
    product_data = {
        "category_id": 1,
        "supplier_id": 5,
        "barcode": "TEST123",
        "name": "Test Product",
        "price": 9.99,
        "cost_price": 5.00,
        "stock_qty": 10
    }
    r = client.post('/products', json=product_data)
    assert r.status_code == 201
    p = r.json()
    pid = p['id']

    # get
    r = client.get(f'/products/{pid}')
    assert r.status_code == 200

    # update invalid (negative price) -> validation 422
    r = client.patch(f'/products/{pid}', json={"price": -1})
    assert r.status_code == 422

    # update valid
    r = client.patch(f'/products/{pid}', json={"price": 12.50})
    assert r.status_code == 200
    assert float(r.json()['price']) == 12.5

    # delete
    r = client.delete(f'/products/{pid}')
    assert r.status_code == 204

    # get missing
    r = client.get(f'/products/{pid}')
    assert r.status_code == 404

def test_create_product_invalid_references(client):
    bad = {
        "category_id": 9999,
        "supplier_id": 9999,
        "barcode": "X",
        "name": "Bad",
        "price": 1.0,
        "cost_price": 1.0,
        "stock_qty": 1
    }
    r = client.post('/products', json=bad)
    assert r.status_code == 400
