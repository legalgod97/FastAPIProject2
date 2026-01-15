import json
from aiokafka import AIOKafkaConsumer

from messaging.exceptions import ConsumerError


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
                await self._process_message(msg)
        finally:
            await self.consumer.stop()

    async def _process_message(self, msg) -> None:
        try:
            payload = json.loads(msg.value.decode())
            event_id = payload["message_id"]

            if await self.processed_repo.exists(event_id):
                await self.consumer.commit()
                return

            await self.processed_repo.mark_processed(event_id)

            await self.consumer.commit()

        except ConsumerError as exc:
            if self.dlq_producer and self.dlq_topic:
                await self.dlq_producer.publish(
                    self.dlq_topic,
                    {
                        "error": str(exc),
                        "raw": msg.value.decode(errors="ignore"),
                    },
                )
                await self.consumer.commit()
