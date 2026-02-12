from typing import Dict, Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
from uuid import UUID, uuid4


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)

    status_tag: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    enriched_value: Mapped[str] = mapped_column(String, nullable=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserModel":
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            status_tag=data.get("status_tag"),
            score=data.get("score"),
            enriched_value=data.get("enriched_value"),
        )

