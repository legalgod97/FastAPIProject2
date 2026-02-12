async def test_get_user_success(client, user_id):
    response = await client.get(f"/users/{user_id}")

    data = response.json()
    assert response.status_code == 200
    assert data["id"] == str(user_id)
    assert data["name"] == "John"
    assert data["status_tag"] == "value"
    assert data["score"] == 42