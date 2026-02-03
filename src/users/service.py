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

        merged_data["extra_field_1"] = f"enriched_{merged_data['extra_field_1']}"
        merged_data["extra_field_2"] = merged_data["extra_field_2"] * 10
        merged_data["enriched_value"] = f"{merged_data['name']}_{merged_data['extra_field_1']}"
        merged_data["computed"] = len(merged_data["name"])

        user_model = UserModel(
            id=merged_data["id"],
            name=merged_data["name"],
            extra_field_1=merged_data["extra_field_1"],
            extra_field_2=merged_data["extra_field_2"],
            enriched_value=merged_data["enriched_value"],
        )

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
                "extra_field_1": db_model.extra_field_1,
                "extra_field_2": db_model.extra_field_2,
            }

        merged_data = {**db_data, **api_data}

        return UserResponse.model_validate(merged_data)
