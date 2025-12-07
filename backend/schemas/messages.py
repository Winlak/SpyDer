from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    user_id: int
    chat_id: str
    chat_title: str | None = None
    external_message_id: str
    from_id: str | None = None
    text: str | None = None
    media_type: str | None = None
    media_url: str | None = None
    created_at: datetime
    mode: str = "userbot"


class MessageEditCreate(BaseModel):
    message_id: int | None = None
    user_id: int
    chat_id: str
    external_message_id: str
    old_text: str | None = None
    new_text: str | None = None
    edited_at: datetime


class MessageDeleteCreate(BaseModel):
    message_id: int | None = None
    user_id: int
    chat_id: str
    external_message_id: str | None = None
    deleted_at: datetime


class DeletedMessageRead(BaseModel):
    text: str | None
    chat_id: str
    chat_title: str | None
    deleted_at: datetime

    class Config:
        from_attributes = True


class MessageEditRead(BaseModel):
    old_text: str | None
    new_text: str | None
    chat_id: str
    chat_title: str | None
    edited_at: datetime

    class Config:
        from_attributes = True
