from typing import Any


class ServiceError(Exception):
    pass


class ServiceRequestError(ServiceError):
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Service returned status {status_code}")


class PermanentServiceError(ServiceError):
    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class TransientServiceError(ServiceError):
    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, *, entity: str, entity_id: Any):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"{entity} with id={entity_id} not found")