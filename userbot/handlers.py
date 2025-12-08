from __future__ import annotations

from datetime import datetime

import httpx
from telethon import events
from telethon.tl.custom.message import Message

from userbot.config import settings

client = httpx.AsyncClient(base_url=settings.backend_api_url, timeout=10.0)


async def bind_handlers(tg_client):
    @tg_client.on(events.NewMessage())
    async def handler_new(event: Message):
        await client.post(
            "/messages/",
            json={
                "user_id": settings.owner_telegram_id,
                "chat_id": str(event.chat_id),
                "external_message_id": str(event.id),
                "from_id": str(event.sender_id),
                "text": event.raw_text,
                "created_at": datetime.utcnow().isoformat(),
                "mode": "userbot",
            },
        )

    @tg_client.on(events.MessageEdited())
    async def handler_edit(event: Message):
        await client.post(
            "/messages/edits/",
            json={
                "user_id": settings.owner_telegram_id,
                "chat_id": str(event.chat_id),
                "external_message_id": str(event.id),
                "old_text": None,
                "new_text": event.raw_text,
                "edited_at": datetime.utcnow().isoformat(),
            },
        )

    @tg_client.on(events.MessageDeleted())
    async def handler_delete(event):
        for msg_id in event.deleted_ids:
            await client.post(
                "/messages/deleted/",
                json={
                    "user_id": settings.owner_telegram_id,
                    "chat_id": str(event.chat_id),
                    "external_message_id": str(msg_id),
                    "deleted_at": datetime.utcnow().isoformat(),
                },
            )
