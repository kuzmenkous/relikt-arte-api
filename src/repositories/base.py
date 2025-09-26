from collections.abc import Iterable
from typing import Any, Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression


class Repository[T](Protocol):
    model: type[T]

    async def get_one(
        self, queries: Iterable[BinaryExpression[Any]], session: AsyncSession
    ) -> T | None:
        stmt = select(self.model).where(*queries)
        result = await session.execute(stmt)
        return result.scalar_one()
