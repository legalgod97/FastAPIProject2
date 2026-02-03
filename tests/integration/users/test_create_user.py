async def test_create_user_success(client):
    payload = {
        "name": "John",
        "extra_field_1": "value",
        "extra_field_2": 42
    }

    response = await client.post("/users/", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["extra_field_1"] == payload["extra_field_1"]
    assert data["extra_field_2"] == payload["extra_field_2"]
