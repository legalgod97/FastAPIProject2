import ujson
from aiokafka import AIOKafkaConsumer
from sqlalchemy.exc import DatabaseError

from messaging.exceptions import InvalidMessageError
from messaging.schemas import DlqMessage


class KafkaConsumerRunner:
    def __init__(
        self,
        *,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        processed_repo,
        dlq_producer=None,
        dlq_topic: str | None = None,
    ):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
        )
        self.processed_repo = processed_repo
        self.dlq_producer = dlq_producer
        self.dlq_topic = dlq_topic

    async def run(self) -> None:
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                await self._process_message(
                    msg,
                    topic=msg.topic,
                    offset=msg.offset,
                )
        finally:
            await self.consumer.stop()

    async def _process_message(
            self,
            msg,
            *,
            topic: str,
            offset: int,
    ) -> None:
        try:
            try:
                raw = msg.value.decode()
            except UnicodeDecodeError as exc:
                raise InvalidMessageError("Invalid UTF-8 payload") from exc

            try:
                payload = ujson.loads(raw)
            except ValueError as exc:
                raise InvalidMessageError("Invalid JSON payload") from exc

            event_id = payload.get("message_id")
            if not event_id:
                raise InvalidMessageError("Missing 'message_id'")

            if await self.processed_repo.exists(event_id):
                await self.consumer.commit()
                return

            await self.processed_repo.mark_processed(event_id)

            await self.consumer.commit()

        except InvalidMessageError as exc:
            if self.dlq_producer and self.dlq_topic:
                dlq_msg = DlqMessage(
                    error=exc.detail,
                    topic=topic,
                    offset=offset,
                    raw_value=msg.value.decode(errors="ignore"),
                )
                await self.dlq_producer.publish(
                    topic=self.dlq_topic,
                    payload=dlq_msg.model_dump(),
                    key=str(offset),
                )
            else:
                raise

        except DatabaseError:
            raise
