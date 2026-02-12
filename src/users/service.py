from uuid import UUID
from typing import Any

from users.exceptions import NotFoundError
from users.schemas import UserCreate, UserResponse
from users.models import UserModel
from users.repository import UserRepository


class UserService:
    def __init__(self, client, repo: UserRepository):
        self._client = client
        self._repo = repo


    async def create_user(self, payload: UserCreate) -> UserResponse:
        api_data = await self._client.create_entity(payload.model_dump())

        merged_data = {**api_data, **payload.model_dump()}

        merged_data["status_tag"] = f"enriched_{merged_data['status_tag']}"
        merged_data["score"] = merged_data["score"] * 10
        merged_data["enriched_value"] = f"{merged_data['name']}_{merged_data['status_tag']}"
        merged_data["name_length"] = len(merged_data["name"])

        user_model = UserModel.from_dict(merged_data)

        await self._repo.create(user_model)

        return UserResponse.model_validate(merged_data)


    async def get_user(self, user_id: UUID) -> UserResponse:
        api_data = await self._client.get_entity(user_id)

        if api_data is None:
            raise NotFoundError(entity="User", entity_id=user_id)

        db_model = await self._repo.get_by_id(user_id)

        db_data: dict[str, Any] = {}
        if db_model:
            db_data = {
                "id": db_model.id,
                "name": db_model.name,
                "status_tag": db_model.status_tag,
                "score": db_model.score,
            }

        merged_data = {**db_data, **api_data}

        return UserResponse.model_validate(merged_data)
