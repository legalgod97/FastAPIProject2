from users.client import FirstService1Client
from users.service import UserService


def get_user_service() -> UserService:
    client = FirstService1Client()
    return UserService(client)