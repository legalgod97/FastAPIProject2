import os
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