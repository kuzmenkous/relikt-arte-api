from src.constants.user import UserRole
from src.schemas.user import UserCreate
from src.services.base import BaseService


class UserService(BaseService):
    async def create_user(self, user_create: UserCreate) -> int:
        if user_create.root.role == UserRole.USER:
            pass
        return 1
