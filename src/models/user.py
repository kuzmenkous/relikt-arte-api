from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.constants.user import ConfirmationCodeType, UserRole
from src.core.db.mixins import IsActiveMixin
from src.models.base import BaseModel


class UserModel(IsActiveMixin, BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(unique=True, index=True)
    full_name: Mapped[str | None]
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(server_default=UserRole.USER.name)

    def __str__(self) -> str:
        return f"User: {self.id}"


class ConfirmationCodeModel(BaseModel):
    __tablename__ = "confirmation_codes"
    __table_args__ = (
        CheckConstraint(
            "code >=100000 AND code <=999999", name="check_code_six_digits"
        ),
    )

    email: Mapped[str] = mapped_column(index=True)
    code: Mapped[int] = mapped_column(unique=True, index=True)
    type: Mapped[ConfirmationCodeType]

    def __str__(self) -> str:
        return f"Confirmation Code: {self.id}"
