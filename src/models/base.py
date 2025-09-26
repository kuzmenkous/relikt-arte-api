import enum
from datetime import datetime
from typing import Any, ClassVar

from sqlalchemy import DateTime, Enum, Identity, MetaData, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData(
    naming_convention={
        # Index naming
        "ix": "ix__%(table_name)s__%(column_0_N_name)s",
        # Unique constraint naming
        "uq": "uq__%(table_name)s__%(column_0_N_name)s",
        # Check constraint naming
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        # Foreign key naming
        "fk": (
            "fk__%(table_name)s__%(column_0_N_name)s__%(referred_table_name)s"
        ),
        # Primary key naming
        "pk": "pk__%(table_name)s",
    }
)


class BaseModel(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Identity(), primary_key=True, sort_order=-1
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), sort_order=100
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), sort_order=100
    )

    metadata = metadata

    type_annotation_map: ClassVar[dict[Any, Any]] = {
        dict[str, Any]: JSONB,
        dict[str, str]: JSONB,
        datetime: DateTime(timezone=True),
        enum.Enum: Enum(enum.Enum, inherit_schema=True),
    }

    def __repr__(self) -> str:
        return self.__str__()
