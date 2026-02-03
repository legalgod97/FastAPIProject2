from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
from uuid import UUID, uuid4


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)

    extra_field_1: Mapped[str] = mapped_column(String, nullable=False)
    extra_field_2: Mapped[int] = mapped_column(Integer, nullable=False)

    enriched_value: Mapped[str] = mapped_column(String, nullable=False)

