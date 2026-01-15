from http import HTTPStatus
from uuid import UUID

import httpx
import ujson
from users.exceptions import TransientServiceError, PermanentServiceError, NotFoundError
from session import settings
from src.utils.retry import retry_async
import logging

logger = logging.getLogger(__name__)


HTTP_TIMEOUT = httpx.Timeout(
    connect=1.0,
    read=3.0,
    write=3.0,
    pool=1.0,
)


class ServiceClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=settings.service1_base_url,
            timeout=HTTP_TIMEOUT,
        )

    @retry_async(
        attempts=3,
        retry_exceptions=(
                httpx.RequestError,
                TransientServiceError,
        ),
    )
    async def get_entity(self, entity_id: UUID) -> dict:
        response = await self._client.get(f"/entities/{entity_id}")

        status = response.status_code

        if status == HTTPStatus.OK:
            return ujson.loads(response.text)

        if status == HTTPStatus.NOT_FOUND:
            logger.info(
                "Entity not found in service",
                extra={"entity": "Entity", "entity_id": entity_id},
            )
            raise NotFoundError(entity="Entity", entity_id=entity_id)

        if HTTPStatus.INTERNAL_SERVER_ERROR <= status:
            logger.warning(
                "Transient error while getting entity",
                extra={"status": status, "entity_id": entity_id},
            )
            raise TransientServiceError(
                message="Transient error while getting entity",
                status_code=status,
            )

        logger.error(
            "Permanent error while getting entity",
            extra={
                "status": status,
                "entity_id": entity_id,
                "response_snippet": response.text[:500],
            },
        )
        raise PermanentServiceError(
            message="Permanent error while getting entity",
            status_code=status,
        )

    @retry_async(
        attempts=3,
        retry_exceptions=(
                httpx.RequestError,
                TransientServiceError,
        ),
    )
    async def create_entity(self, payload: dict) -> dict:
        response = await self._client.post(
            "/entities",
            json=payload,
        )

        status = response.status_code

        if HTTPStatus.OK <= status < HTTPStatus.BAD_REQUEST:
            return ujson.loads(response.text)

        if HTTPStatus.INTERNAL_SERVER_ERROR <= status:
            logger.warning(
                "Transient error while creating entity",
                extra={
                    "status": status,
                    "entity_id": payload.get("id"),
                },
            )
            raise TransientServiceError(
                message="Transient error while creating entity",
                status_code=status,
            )

        logger.error(
            "Permanent error while creating entity",
            extra={
                "status": status,
                "response": response.text,
            },
        )
        raise PermanentServiceError(
            message="Permanent error while creating entity",
            status_code=status,
        )