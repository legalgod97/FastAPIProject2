from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from users.schemas import UserCreate
from users.service import UserService


async def test_get_user_success():
    user_id = uuid4()

    client = AsyncMock()
    client.get_entity.return_value = {
        "id": user_id,
        "name": "John",
        "extra_field_1": "value",
        "extra_field_2": 42,
    }

    service = UserService(client)

    user = await service.get_user(user_id)

    client.get_entity.assert_awaited_once_with(user_id)

    assert user.id == user_id
    assert user.name == "John"
    assert user.extra_field_1 == "value"
    assert user.extra_field_2 == 42


async def test_create_user():
    user_id = uuid4()

    client = AsyncMock()
    client.create_entity.return_value = {
        "id": user_id,
        "name": "John",
        "extra_field_1": "value",
        "extra_field_2": 42,
    }

    service = UserService(client)

    payload = UserCreate(
        name="John",
        extra_field_1="value",
        extra_field_2=42,
    )

    user = await service.create_user(payload)

    client.create_entity.assert_awaited_once_with(payload.model_dump())

    assert user.id == user_id
    assert user.name == "John"
    assert user.extra_field_1 == "value"
    assert user.extra_field_2 == 42



async def test_get_user_not_found():
    user_id = uuid4()

    client = AsyncMock()
    client.get_entity.return_value = None

    service = UserService(client)

    with pytest.raises(ValidationError):
        await service.get_user(user_id)

    client.get_entity.assert_awaited_once_with(user_id)