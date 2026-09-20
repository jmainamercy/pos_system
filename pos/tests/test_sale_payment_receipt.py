def test_sale_payment_and_receipt_flow(client):
    # create customer
    cust = {"first_name": "Buyer", "last_name": "One"}
    r = client.post('/customers', json=cust)
    assert r.status_code == 201
    customer_id = r.json()['id']

    # create a product to sell
    product_data = {
        "category_id": 1,
        "supplier_id": 5,
        "barcode": "SOLD1",
        "name": "Sold Product",
        "price": 10.00,
        "cost_price": 5.00,
        "stock_qty": 5
    }
    r = client.post('/products', json=product_data)
    assert r.status_code == 201
    product = r.json()
    pid = product['id']

    # check unpaid status (no sale yet) via payment status endpoint -> 404 (sale missing)
    r = client.get('/payments/sale/9999/status')
    assert r.status_code == 404

    # create sale
    sale_payload = {"customer_id": customer_id, "discount": 0.00, "items": [{"product_id": pid, "quantity": 2}]}
    r = client.post('/sales', json=sale_payload)
    assert r.status_code == 201
    sale = r.json()
    sale_id = sale['id']
    assert float(sale['final_amount']) >= 0

    # check payment status unpaid
    r = client.get(f'/payments/sale/{sale_id}/status')
    assert r.status_code == 200
    assert r.json()['status'] in ("UNPAID", "PARTIALLY_PAID")

    # partial payment
    pay = {"sale_id": sale_id, "payment_method": "Card", "amount_paid": 5.00}
    r = client.post('/payments', json=pay)
    assert r.status_code == 201

    # overpayment (non-cash) should be rejected
    pay_over = {"sale_id": sale_id, "payment_method": "Card", "amount_paid": 9999.00}
    r = client.post('/payments', json=pay_over)
    assert r.status_code == 400

    # finish payment (cash overpayment allowed) - use remaining balance as cash
    status_before = client.get(f'/payments/sale/{sale_id}/status').json()
    remaining = float(status_before['remaining_balance'])
    if remaining > 0:
        pay_cash = {"sale_id": sale_id, "payment_method": "Cash", "amount_paid": remaining}
        r = client.post('/payments', json=pay_cash)
        assert r.status_code == 201

    # now can issue receipt
    r = client.post(f'/receipts/sale/{sale_id}')
    assert r.status_code == 201
    receipt = r.json()
    assert 'receipt_number' in receipt
