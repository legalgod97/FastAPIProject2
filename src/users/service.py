from typing import Any
from uuid import UUID

from users.client import ServiceClient
from users.schemas import UserCreate, UserResponse


class UserService:
    def __init__(self, client: ServiceClient):
        self._client = client

    async def create_user(self, payload: UserCreate) -> UserResponse:
        data: dict[str, Any] = await self._client.create_entity(
            payload.model_dump()
        )
        return UserResponse.model_validate(data)

    async def get_user(self, user_id: UUID) -> UserResponse:
        data: dict[str, Any] = await self._client.get_entity(user_id)
        return UserResponse.model_validate(data)
