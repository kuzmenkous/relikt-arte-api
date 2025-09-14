from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..config import settings

engine: AsyncEngine = create_async_engine(
    settings.db.url,
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=15,
)
session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False
)
