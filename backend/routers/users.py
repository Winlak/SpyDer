from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_session
from backend.schemas.users import UserCreate, UserModeUpdate, UserRead
from backend.services.users import get_user_by_telegram_id, upsert_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_or_update_user(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await upsert_user(session, telegram_id=payload.telegram_id, is_premium=payload.is_premium)
    return user


@router.get("/{telegram_id}", response_model=UserRead)
async def get_user(telegram_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/mode")
async def set_mode(payload: UserModeUpdate, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_telegram_id(session, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # placeholder for saving mode choice
    return {"user_id": user.telegram_id, "mode": payload.mode}
