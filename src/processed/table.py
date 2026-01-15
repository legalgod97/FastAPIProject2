from datetime import datetime, UTC

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class ProcessedMessage(Base):
    __tablename__ = "processed_messages"

    event_id: Mapped[str] = mapped_column(String, primary_key=True)
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    )