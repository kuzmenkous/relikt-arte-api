from fastapi import APIRouter

from src.dependencies.db import Session
from src.schemas.user import UserCreate
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_description="Id of the created user")
async def create_user(session: Session, user_create: UserCreate) -> int:
    return await UserService(session).create_user(user_create)
