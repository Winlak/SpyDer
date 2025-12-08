from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: int
    is_premium: bool | None = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserModeUpdate(BaseModel):
    user_id: int
    mode: str
