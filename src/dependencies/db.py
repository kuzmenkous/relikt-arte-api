from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db.session import get_async_session

session = Annotated[AsyncSession, Depends(get_async_session)]
