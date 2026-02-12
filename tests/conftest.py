import os
os.environ["POSTGRES_URL"] = "postgresql+asyncpg://test:test@localhost:5431/test"
os.environ["SERVICE1_BASE_URL"] = "http://fake"

from users.schemas import UserResponse, UserCreate

from unittest.mock import AsyncMock
from uuid import uuid4, UUID

from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from processed.table import Base
from users.repository import UserRepository
from users.service import UserService

from types import SimpleNamespace

from users.dependencies import get_user_service

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


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
                status_tag=payload.status_tag,
                score=payload.score,
                enriched_value="mock_enriched",
            )

        async def get_user(self, user_id: UUID):
            return UserResponse(
                id=user_id,
                name="John",
                status_tag="value",
                score=42,
                enriched_value="mock_enriched",
            )

    return MockService()


class MockClientNotFound:
    async def get_entity(self, user_id: UUID):
        return None


@pytest.fixture
def mock_client_not_found():
    return MockClientNotFound()


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:14") as postgres:
        postgres.USER = "test"
        postgres.PASSWORD = "test"
        postgres.DBNAME = "test"

        host = postgres.get_container_host_ip()
        port = postgres.get_exposed_port(5432)

        async_url = f"postgresql+asyncpg://{postgres.USER}:{postgres.PASSWORD}@{host}:{port}/{postgres.DBNAME}"
        yield async_url


@pytest.fixture
async def db_session(postgres_container):
    engine = create_async_engine(postgres_container, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def user_service(mock_client, user_repository):
    return UserService(
        client=mock_client,
        repo=user_repository
    )


@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)


@pytest.fixture
def mock_client(user_id):
    client = AsyncMock()
    client.create_entity.return_value = {
        "id": user_id,
        "name": "John",
        "status_tag": "status_tag",
        "score": 42,
    }
    client.get_entity.return_value = {
        "id": user_id,
        "name": "John",
        "status_tag": "value",
        "score": 42,
    }
    return client

