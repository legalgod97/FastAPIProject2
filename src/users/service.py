from typing import Protocol, Any
from uuid import UUID

from users.schemas import UserCreate, UserResponse


class UserClient(Protocol):
    async def create_entity(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...

    async def get_entity(self, user_id: UUID) -> dict[str, Any]:
        ...


class UserService:
    def __init__(self, client: UserClient):
        self._client = client

    async def create_user(self, payload: UserCreate) -> UserResponse:
        data = await self._client.create_entity(payload.model_dump())
        return UserResponse.model_validate(data)

    async def get_user(self, user_id: UUID) -> UserResponse:
        data = await self._client.get_entity(user_id)
        return UserResponse.model_validate(data)

