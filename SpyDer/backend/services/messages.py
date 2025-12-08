from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import Chat, DeletedMessage, Message, MessageEdit


async def get_or_create_chat(session: AsyncSession, user_id: int, chat_id: str, title: str | None, mode: str) -> Chat:
    result = await session.execute(
        select(Chat).where(Chat.user_id == user_id, Chat.chat_id == chat_id)
    )
    chat = result.scalar_one_or_none()
    if chat is None:
        chat = Chat(user_id=user_id, chat_id=chat_id, title=title, mode=mode)
        session.add(chat)
        await session.flush()
    else:
        if title and not chat.title:
            chat.title = title
    return chat


async def create_message(session: AsyncSession, payload: dict) -> Message:
    chat = await get_or_create_chat(
        session,
        user_id=payload["user_id"],
        chat_id=payload["chat_id"],
        title=payload.get("chat_title"),
        mode=payload.get("mode", "userbot"),
    )
    message = Message(
        user_id=payload["user_id"],
        chat_id=chat.id,
        external_message_id=str(payload["external_message_id"]),
        from_id=payload.get("from_id"),
        text=payload.get("text"),
        media_type=payload.get("media_type"),
        media_url=payload.get("media_url"),
        created_at=payload.get("created_at", datetime.utcnow()),
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def record_edit(session: AsyncSession, payload: dict) -> MessageEdit:
    message = await _get_message_by_external(
        session,
        user_id=payload["user_id"],
        chat_id=payload["chat_id"],
        external_id=payload["external_message_id"],
    )
    old_text = message.text if message else None
    if message is None:
        message = await create_message(
            session,
            {
                "user_id": payload["user_id"],
                "chat_id": payload["chat_id"],
                "chat_title": None,
                "external_message_id": payload["external_message_id"],
                "text": payload.get("new_text"),
                "created_at": datetime.utcnow(),
            },
        )
    edit = MessageEdit(
        message_id=message.id,
        old_text=old_text,
        new_text=payload.get("new_text"),
        edited_at=payload.get("edited_at", datetime.utcnow()),
    )
    message.text = payload.get("new_text")
    session.add(edit)
    await session.commit()
    await session.refresh(edit)
    return edit


async def record_delete(session: AsyncSession, payload: dict) -> DeletedMessage:
    message = None
    if payload.get("external_message_id"):
        message = await _get_message_by_external(
            session,
            user_id=payload["user_id"],
            chat_id=payload["chat_id"],
            external_id=payload["external_message_id"],
        )
    if message is None and payload.get("message_id"):
        message = await session.get(Message, payload["message_id"])
    if message is None:
        chat = await get_or_create_chat(
            session,
            user_id=payload["user_id"],
            chat_id=payload["chat_id"],
            title=None,
            mode="userbot",
        )
        message = Message(
            user_id=payload["user_id"],
            chat_id=chat.id,
            external_message_id=str(payload.get("external_message_id") or "0"),
            created_at=datetime.utcnow(),
            text=None,
        )
        session.add(message)
        await session.flush()
    message.is_deleted = True
    deletion = DeletedMessage(
        message_id=message.id, deleted_at=payload.get("deleted_at", datetime.utcnow())
    )
    session.add(deletion)
    await session.commit()
    await session.refresh(deletion)
    return deletion


async def _get_message_by_external(
    session: AsyncSession, user_id: int, chat_id: str, external_id: str
) -> Message | None:
    stmt = (
        select(Message)
        .join(Chat)
        .where(
            Message.external_message_id == str(external_id),
            Chat.chat_id == chat_id,
            Chat.user_id == user_id,
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def fetch_deleted(session: AsyncSession, user_id: int, limit: int) -> list[DeletedMessage]:
    stmt = (
        select(DeletedMessage)
        .join(Message)
        .join(Chat)
        .where(Message.user_id == user_id)
        .order_by(DeletedMessage.deleted_at.desc())
        .limit(limit)
    )
    res = await session.execute(stmt)
    return res.scalars().all()


async def fetch_edits(session: AsyncSession, user_id: int, limit: int) -> list[MessageEdit]:
    stmt = (
        select(MessageEdit)
        .join(Message)
        .join(Chat)
        .where(Message.user_id == user_id)
        .order_by(MessageEdit.edited_at.desc())
        .limit(limit)
    )
    res = await session.execute(stmt)
    return res.scalars().all()
