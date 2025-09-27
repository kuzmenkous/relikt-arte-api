from functools import cached_property
from typing import Annotated, Self

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    computed_field,
    model_validator,
)

from src.constants.user import password_hasher


class EmailUpdate(BaseModel):
    email: EmailStr


Password = Annotated[SecretStr, Field(min_length=6)]
_PasswordForCheck = Annotated[Password, Field(exclude=True)]


class PasswordCreate(BaseModel):
    password: _PasswordForCheck

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def hashed_password(self) -> str:
        return password_hasher.hash(self.password.get_secret_value())


class PasswordUpdate(PasswordCreate):
    password2: _PasswordForCheck

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password == self.password2:
            return self
        raise ValueError("passwords don't match")
