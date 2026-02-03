from unittest.mock import AsyncMock
from uuid import uuid4, UUID

import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from processed.table import Base
from users.repository import UserRepository
from users.service import UserService


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
        "extra_field_1": "value",
        "extra_field_2": 42,
    }
    client.get_entity.return_value = {
        "id": user_id,
        "name": "John",
        "extra_field_1": "value",
        "extra_field_2": 42,
    }
    return client
