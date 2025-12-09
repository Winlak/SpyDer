from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import User


async def upsert_user(session: AsyncSession, telegram_id: int, is_premium: bool | None = None) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            telegram_id=telegram_id,
            is_premium=is_premium if is_premium is not None else False,
        )
        session.add(user)
    else:
        if is_premium is not None:
            user.is_premium = is_premium

    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()
