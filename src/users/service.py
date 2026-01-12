from users.client import FirstService1Client


class UserService:
    def __init__(self, client: FirstService1Client):
        self._client = client

    async def create_user(self, payload: dict) -> dict:
        return await self._client.create_entity(payload)

    async def get_user(self, user_id) -> dict:
        return await self._client.get_entity(user_id)
