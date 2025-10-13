from typing import Annotated

from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from src.constants.user import UserRole
from src.models.user import UserModel
from src.schemas.user import PasswordCreate, _PasswordForCheck


class SuperadminCredentials(PasswordCreate, BaseSettings):
    email: Annotated[EmailStr, Field(validation_alias="SUPERADMIN_EMAIL")]
    password: Annotated[
        _PasswordForCheck, Field(validation_alias="SUPERADMIN_PASSWORD")
    ]


superadmin_credentials = SuperadminCredentials()


async def insert_first_rows_with_async_connection(
    async_connection: AsyncConnection,
) -> None:
    session = AsyncSession(async_connection)
    await create_first_rows(session)
    await session.flush()


async def create_first_rows(session: AsyncSession) -> None:
    # Create superuser
    user = UserModel(
        role=UserRole.SUPERADMIN, **superadmin_credentials.model_dump()
    )
    session.add(user)
