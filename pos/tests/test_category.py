def test_category_crud(client):
    # list (seeded)
    r = client.get("/categories")
    assert r.status_code == 200

    # create
    payload = {"name": "New Cat", "description": "desc"}
    r = client.post("/categories", json=payload)
    assert r.status_code == 201
    created = r.json()
    cid = created["id"]
    assert created["name"] == payload["name"]

    # get
    r = client.get(f"/categories/{cid}")
    assert r.status_code == 200

    # update
    r = client.patch(f"/categories/{cid}", json={"description": "updated"})
    assert r.status_code == 200
    assert r.json()["description"] == "updated"

    # delete
    r = client.delete(f"/categories/{cid}")
    assert r.status_code == 204

    # missing
    r = client.get(f"/categories/{cid}")
    assert r.status_code == 404
