def test_customer_crud_and_validation(client):
    # create
    payload = {"first_name": "Jane", "last_name": "Doe"}
    r = client.post("/customers", json=payload)
    assert r.status_code == 201
    cust = r.json()
    cid = cust["id"]

    # validation error (missing required)
    r = client.post("/customers", json={"last_name": "NoFirst"})
    assert r.status_code == 422

    # update
    r = client.patch(f"/customers/{cid}", json={"phone_number": "000"})
    assert r.status_code == 200
    assert r.json()["phone_number"] == "000"

    # delete
    r = client.delete(f"/customers/{cid}")
    assert r.status_code == 204

    # missing
    r = client.get(f"/customers/{cid}")
    assert r.status_code == 404
