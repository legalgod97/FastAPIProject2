from uuid import uuid4
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from main import app
from users.schemas import UserResponse


async def test_create_user_success():
    user_id = uuid4()

    from users.dependencies import get_user_service
    async def mock_service():
        class MockService:
            async def create_user(self, payload):
                return UserResponse(
                    id=user_id,
                    name=payload.name,
                    extra_field_1=payload.extra_field_1,
                    extra_field_2=payload.extra_field_2,
                )

        return MockService()

    app.dependency_overrides[get_user_service] = mock_service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "name": "John",
            "extra_field_1": "value",
            "extra_field_2": 42,
        }
        response = await client.post("/users/", json=payload)

    data = response.json()
    assert response.status_code == 200
    assert data["id"] == str(user_id)
    assert data["name"] == payload["name"]
    assert data["extra_field_1"] == payload["extra_field_1"]
    assert data["extra_field_2"] == payload["extra_field_2"]

    app.dependency_overrides.clear()



