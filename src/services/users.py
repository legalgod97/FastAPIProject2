from uuid import UUID

from src.clients.users import UsersApiClient
from src.schemas.users import UserCreate, UserResponse


class UserService:
    def __init__(self, client: UsersApiClient) -> None:
        self._client = client

    async def create_user(self, payload: UserCreate) -> UserResponse:
        data = await self._client.create_user(payload.model_dump())
        return UserResponse.model_validate(data)

    async def get_user(self, user_id: UUID) -> UserResponse:
        data = await self._client.get_user(user_id)
        return UserResponse.model_validate(data)
