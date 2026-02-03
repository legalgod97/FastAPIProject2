import os
from uuid import uuid4, UUID

from users.schemas import UserResponse, UserCreate

os.environ["POSTGRES_URL"] = "postgresql+asyncpg://test:test@localhost:5431/test"
os.environ["SERVICE1_BASE_URL"] = "http://fake"
from types import SimpleNamespace
from unittest.mock import AsyncMock

from users.dependencies import get_user_service

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.fixture
def mock_user_service():
    mock_service = AsyncMock()
    mock_service._client = AsyncMock()
    return mock_service


@pytest.fixture
async def client(mock_user_service):
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    fake_settings = SimpleNamespace(
        postgres_url="postgresql+asyncpg://test:test@localhost:5431/test",
        redis_host="localhost",
        redis_port=6379,
        redis_db=0,
        cache_ttl=3600,
        service1_base_url="http://test-service",
    )

    monkeypatch.setattr("src.config.config.get_settings", lambda: fake_settings)



@pytest.fixture
def user_id():
    return uuid4()

@pytest.fixture
def mock_user_service():
    class MockService:
        async def create_user(self, payload: UserCreate):
            return UserResponse(
                id=uuid4(),
                name=payload.name,
                extra_field_1=payload.extra_field_1,
                extra_field_2=payload.extra_field_2,
                enriched_value="mock_enriched",
            )

        async def get_user(self, user_id: UUID):
            return UserResponse(
                id=user_id,
                name="John",
                extra_field_1="value",
                extra_field_2=42,
                enriched_value="mock_enriched",
            )

    return MockService()

@pytest.fixture
async def client(mock_user_service):
    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()