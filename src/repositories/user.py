from src.models.user import ConfirmationCodeModel, UserModel
from src.repositories.base import Repository
from src.schemas.user import UserCreate


class UserRepository:
    _repository: Repository[UserModel]

    async def create_user(self, user_create: UserCreate) -> UserModel:
        return UserModel(**user_create.model_dump())


class ConfirmationCodeRepository:
    _repository: Repository[ConfirmationCodeModel]
