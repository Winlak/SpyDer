from __future__ import annotations

import asyncio
from typing import Optional

from telethon import TelegramClient
from telethon.sessions import StringSession

from userbot.config import settings


class ClientManager:
    def __init__(self) -> None:
        self._client: Optional[TelegramClient] = None

    def get_client(self) -> TelegramClient:
        if self._client is None:
            session = StringSession(settings.session_string) if settings.session_string else StringSession()
            self._client = TelegramClient(session, settings.api_id, settings.api_hash)
        return self._client

    async def start(self) -> TelegramClient:
        client = self.get_client()
        await client.start()
        return client


manager = ClientManager()
