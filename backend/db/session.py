from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.config import settings


class Base(DeclarativeBase):
    pass


def get_engine():
    return create_async_engine(settings.database_url, echo=False, future=True)


def get_session_factory(engine=None) -> async_sessionmaker[AsyncSession]:
    engine = engine or get_engine()
    return async_sessionmaker(engine, expire_on_commit=False)


engine = get_engine()
async_session = get_session_factory(engine)


async def get_session():
    async with async_session() as session:
        yield session
