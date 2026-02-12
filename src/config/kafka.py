from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(
        default="localhost:29092",
        env="KAFKA_BOOTSTRAP_SERVERS",
    )

    users_created_topic: str = "users.created"
    users_updated_topic: str = "users.updated"
    users_deleted_topic: str = "users.deleted"

    group_id: str = "profiles-service"

    class Config:
        env_file = ".env"