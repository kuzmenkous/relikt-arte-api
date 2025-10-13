from functools import cached_property
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    RootModel,
    SecretStr,
    computed_field,
    model_validator,
)
from pydantic_extra_types.phone_numbers import (
    PhoneNumber,
    PhoneNumberValidator,
)

from src.constants.user import ConfirmationCodeType, UserRole, password_hasher
from src.schemas.base import CreatedAtMixin, IdSchema, IsActiveMixin


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


UAPhoneNumberType = Annotated[
    str | PhoneNumber,
    PhoneNumberValidator(supported_regions=["UA"], number_format="E164"),
]


class PhoneMixin:
    phone: UAPhoneNumberType


class UserBase[T](BaseModel, from_attributes=True):
    role: Annotated[T, Field(description="Not updating!")]


class UserCreateBase[T](EmailUpdate, PasswordUpdate, UserBase[T]):
    pass


class SuperadminCreate(UserCreateBase[Literal[UserRole.SUPERADMIN]]):
    pass


class AdminsUserCreate(UserCreateBase[Literal[UserRole.ADMIN]]):
    pass


class RegularUserCreate(PhoneMixin, UserCreateBase[Literal[UserRole.USER]]):
    pass


UserCreate = RootModel[
    Annotated[
        AdminsUserCreate | SuperadminCreate | RegularUserCreate,
        Field(discriminator="role"),
    ]
]


class UserUpdateBase[T](UserBase[T]):
    pass


class SuperadminUpdate(
    EmailUpdate, UserUpdateBase[Literal[UserRole.SUPERADMIN]]
):
    pass


class AdminsUserUpdate(EmailUpdate, UserUpdateBase[Literal[UserRole.ADMIN]]):
    pass


class RegularUserUpdate(PhoneMixin, UserUpdateBase[Literal[UserRole.USER]]):
    full_name: str | None = None


UserUpdate = RootModel[
    Annotated[
        SuperadminUpdate | AdminsUserUpdate | RegularUserUpdate,
        Field(discriminator="role"),
    ]
]


class UserRead(IdSchema, UserBase[UserRole], IsActiveMixin, CreatedAtMixin):
    pass


class SuperadminRead(SuperadminUpdate, UserRead):
    pass


class AdminsUserRead(AdminsUserUpdate, UserRead):
    pass


class RegularUserRead(RegularUserUpdate, UserRead):
    pass


User = RootModel[
    Annotated[
        SuperadminRead | AdminsUserRead | RegularUserRead,
        Field(discriminator="role"),
    ]
]


class ConfirmationCodeWrite(EmailUpdate, BaseModel):
    code: str
    type: ConfirmationCodeType


class ConfirmationCodeRead(IdSchema, ConfirmationCodeWrite, CreatedAtMixin):
    pass
