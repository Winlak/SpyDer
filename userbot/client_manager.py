from __future__ import annotations

from typing import Optional

from telethon import TelegramClient
from telethon.sessions import StringSession


class ClientManager:
    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session_string: str,
        backend_api_url: str,
    ) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_string = session_string
        self.backend_api_url = backend_api_url
        self._client: Optional[TelegramClient] = None

    def get_client(self) -> TelegramClient:
        if self._client is None:
            self._client = TelegramClient(
                StringSession(self.session_string),
                self.api_id,
                self.api_hash,
            )
        return self._client

    async def start(self) -> TelegramClient:
        client = self.get_client()
        await client.start()
        return client

    async def run_forever(self) -> None:
        if self._client is None:
            return
        await self._client.run_until_disconnected()
