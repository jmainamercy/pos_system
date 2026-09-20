def test_supplier_crud(client):
    # list (seeded)
    r = client.get('/suppliers')
    assert r.status_code == 200

    # create
    payload = {"company_name": "Acme Ltd", "phone": "12345"}
    r = client.post('/suppliers', json=payload)
    assert r.status_code == 201
    created = r.json()
    sid = created['id']

    # get
    r = client.get(f'/suppliers/{sid}')
    assert r.status_code == 200

    # update
    r = client.patch(f'/suppliers/{sid}', json={"phone": "54321"})
    assert r.status_code == 200
    assert r.json()['phone'] == '54321'

    # delete
    r = client.delete(f'/suppliers/{sid}')
    assert r.status_code == 204

    # missing
    r = client.get(f'/suppliers/{sid}')
    assert r.status_code == 404
