import asyncio
import uvicorn
from fastapi import FastAPI
from config.config import get_settings
from messaging.consumer import KafkaConsumerRunner
from processed.repository import ProcessedMessageRepository
import contextlib
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


settings = get_settings()

engine = create_async_engine(settings.database_url, echo=False)
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

@contextlib.asynccontextmanager
async def lifespan_handler(application: FastAPI):
    session = async_session_factory()
    processed_repo = ProcessedMessageRepository(session)

    consumer_runner = KafkaConsumerRunner(
        bootstrap_servers=settings.kafka.bootstrap_servers,
        topic=settings.kafka.topic,
        group_id=settings.kafka.group_id,
        processed_repo=processed_repo,
    )

    consumer_task = asyncio.create_task(consumer_runner.run())
    application.state.consumer_task = consumer_task

    try:
        yield
    finally:
        consumer_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await consumer_task

app = FastAPI(lifespan=lifespan_handler)

@app.get("/")
async def root():
    return {"message": "Consumer service running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)