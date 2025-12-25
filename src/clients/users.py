from uuid import UUID

import httpx


class UsersApiClient:
    def __init__(self, base_url: str):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=5.0,
        )

    async def create_user(self, payload: dict) -> dict:
        response = await self._client.post("/users", json=payload)
        response.raise_for_status()
        return response.json()

    async def get_user(self, user_id: UUID) -> dict:
        response = await self._client.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()