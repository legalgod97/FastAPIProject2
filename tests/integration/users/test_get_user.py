from uuid import uuid4, UUID
from users.dependencies import get_user_service
from httpx._transports.asgi import ASGITransport
from httpx import AsyncClient
from main import app
from users.schemas import UserResponse


async def test_get_user_success():

    user_id = uuid4()

    async def mock_service():
        class MockService:
            async def get_user(self, id: UUID):
                return UserResponse(
                    id=user_id,
                    name="John",
                    extra_field_1="value",
                    extra_field_2=42,
                )
        return MockService()

    app.dependency_overrides[get_user_service] = mock_service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/users/{user_id}")

    data = response.json()
    assert response.status_code == 200
    assert data["id"] == str(user_id)
    assert data["name"] == "John"
    assert data["extra_field_1"] == "value"
    assert data["extra_field_2"] == 42

    app.dependency_overrides.clear()