from fastapi import APIRouter
from uuid import UUID

from src.clients.users import UsersApiClient
from src.schemas.users import UserCreate, UserResponse
from src.services.users import UserService

client = UsersApiClient(base_url="http://user-service:8000")
user_service = UserService(client)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(payload: UserCreate) -> UserResponse:
    return await user_service.create_user(payload)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID) -> UserResponse:
    return await user_service.get_user(user_id)