from enum import StrEnum, auto, unique

from argon2 import PasswordHasher


@unique
class UserRole(StrEnum):
    USER = auto()
    ADMIN = auto()
    SUPERADMIN = auto()


class ConfirmationCodeType(StrEnum):
    REGISTRATION = auto()
    EMAIL_CHANGE = auto()
    PASSWORD_RESET = auto()


password_hasher = PasswordHasher()
