import httpx

from users.exceptions import ServiceRequestError
from session import settings

from src.utils.retry import retry_async


class FirstService1Client:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=settings.service1_base_url,
            timeout=5.0,
        )

    @retry_async(
        attempts=3,
        retry_exceptions=(httpx.RequestError, ServiceRequestError),
    )
    async def get_entity(self, entity_id: int) -> dict:
        response = await self._client.get(f"/entities/{entity_id}")

        if response.status_code != 200:
            raise ServiceRequestError(response.status_code)

        return response.json()

    @retry_async(
        attempts=3,
        retry_exceptions=(httpx.RequestError, ServiceRequestError),
    )
    async def create_entity(self, payload: dict) -> dict:
        response = await self._client.post(
            "/entities",
            json=payload,
        )

        if response.status_code != 200:
            raise ServiceRequestError(response.status_code)

        return response.json()