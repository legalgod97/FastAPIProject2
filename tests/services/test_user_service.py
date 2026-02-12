from uuid import uuid4

import pytest

from users.exceptions import NotFoundError
from users.repository import UserRepository
from users.schemas import UserCreate
from users.service import UserService


@pytest.mark.asyncio
async def test_create_user_success(user_service):
    payload = UserCreate(
        name="John",
        status_tag="value",
        score=42,
    )

    user = await user_service.create_user(payload)

    assert user.id is not None
    assert user.name == "John"
    assert user.status_tag == "enriched_value"
    assert user.score == 420
    assert user.enriched_value == "John_enriched_value"


@pytest.mark.asyncio
async def test_get_user_not_found(db_session, mock_client_not_found):
    repo = UserRepository(db_session)
    service = UserService(client=mock_client_not_found, repo=repo)

    with pytest.raises(NotFoundError):
        await service.get_user(uuid4())