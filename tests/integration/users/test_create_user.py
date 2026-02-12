async def test_create_user_success(client):
    payload = {
        "name": "John",
        "status_tag": "value",
        "score": 42
    }

    response = await client.post("/users/", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["status_tag"] == payload["status_tag"]
    assert data["score"] == payload["score"]
