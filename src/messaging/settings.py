from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(
        default="localhost:29092",
        env="KAFKA_BOOTSTRAP_SERVERS",
    )

    users_created_topic: str = Field(
        default="users.created",
        env="KAFKA_USERS_CREATED_TOPIC",
    )

    users_updated_topic: str = Field(
        default="users.updated",
        env="KAFKA_USERS_UPDATED_TOPIC",
    )

    users_deleted_topic: str = Field(
        default="users.deleted",
        env="KAFKA_USERS_DELETED_TOPIC",
    )