from users.client import ServiceClient
from users.service import UserService


def get_user_service() -> UserService:
    client = ServiceClient()
    return UserService(client)