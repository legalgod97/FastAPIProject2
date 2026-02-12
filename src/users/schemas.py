from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    id: UUID
    name: str


class UserResponse(UserBase):
    status_tag: str
    score: int
    enriched_value: str


class UserCreate(BaseModel):
    name: str
    status_tag: str
    score: int