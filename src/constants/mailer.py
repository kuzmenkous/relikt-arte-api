from enum import StrEnum, auto, unique


@unique
class EmailType(StrEnum):
    TEXT = auto()
    HTML = auto()
