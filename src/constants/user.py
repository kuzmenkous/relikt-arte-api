from enum import StrEnum, auto, unique

from argon2 import PasswordHasher


@unique
class UserRole(StrEnum):
    USER = auto()
    ADMIN = auto()
    SUPERADMIN = auto()


password_hasher = PasswordHasher()
