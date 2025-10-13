from datetime import datetime
from pathlib import Path

from sqlalchemy import Identity, func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.mailer.settings import settings
from src.schemas.mailer import EmailSend

DATABASE_PATH = Path(settings.mailer_data_path) / "mailer.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class EmailModel(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(
        Identity(), primary_key=True, sort_order=-1
    )
    email: Mapped[str]
    subject: Mapped[str]
    body: Mapped[str]
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), sort_order=100
    )


engine = create_async_engine(DATABASE_URL, echo=settings.debug)
session_getter = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_emails(send_data: EmailSend, status: str) -> None:
    async with session_getter.begin() as session:
        email_objs = [
            EmailModel(
                email=email,
                subject=send_data.subject,
                body=send_data.body,
                status=status,
            )
            for email in send_data.emails
        ]
        session.add_all(email_objs)
