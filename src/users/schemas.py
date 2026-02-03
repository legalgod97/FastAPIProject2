from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    id: UUID
    name: str


class UserResponse(UserBase):
    extra_field_1: str
    extra_field_2: int
    enriched_value: str


class UserCreate(BaseModel):
    name: str
    extra_field_1: str
    extra_field_2: int