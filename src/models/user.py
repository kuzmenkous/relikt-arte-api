from sqlalchemy.orm import Mapped, mapped_column

from ..constants.user import UserRole
from ..core.db.mixins import IsActiveMixin
from .base import BaseModel


class UserModel(IsActiveMixin, BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(unique=True, index=True)
    full_name: Mapped[str | None]
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(server_default=UserRole.USER.name)

    def __str__(self) -> str:
        return f"User: {self.id}"
