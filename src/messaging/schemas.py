from datetime import datetime, UTC
from uuid import UUID
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: UUID
    event_type: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UserUpdatedEvent(BaseEvent):
    event_type: str = "user.updated"

    user_id: UUID
    name: str
