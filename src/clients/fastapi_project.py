import httpx

from session import settings


class Service1Client:
    def __init__(self):
        self.base_url = settings.service1_base_url

    async def get_entity(self, entity_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/entities/{entity_id}"
            )
            response.raise_for_status()
            return response.json()

    async def create_entity(self, payload: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/entities",
                json=payload
            )
            response.raise_for_status()
            return response.json()