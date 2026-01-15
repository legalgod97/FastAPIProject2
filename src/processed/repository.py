from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from processed.table import ProcessedMessage


class ProcessedMessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, event_id: str) -> bool:
        result = await self.session.execute(
            select(ProcessedMessage.event_id)
            .where(ProcessedMessage.event_id == event_id)
        )
        return result.scalar_one_or_none() is not None

    async def mark_processed(self, event_id: str) -> None:
        self.session.add(
            ProcessedMessage(event_id=event_id)
        )
