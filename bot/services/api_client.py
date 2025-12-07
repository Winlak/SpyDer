from __future__ import annotations

from typing import Any

import httpx

from bot.config import settings


class BackendClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url=settings.backend_api_url, timeout=10.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def upsert_user(self, telegram_id: int, is_premium: bool | None = None) -> Any:
        payload = {"telegram_id": telegram_id, "is_premium": is_premium}
        resp = await self._client.post("/users/", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def get_last_deleted(self, user_id: int, limit: int = 10) -> Any:
        resp = await self._client.get("/messages/deleted", params={"user_id": user_id, "limit": limit})
        resp.raise_for_status()
        return resp.json()

    async def get_last_edited(self, user_id: int, limit: int = 10) -> Any:
        resp = await self._client.get("/messages/edited", params={"user_id": user_id, "limit": limit})
        resp.raise_for_status()
        return resp.json()

    async def mark_mode(self, user_id: int, mode: str) -> Any:
        resp = await self._client.post("/users/mode", json={"user_id": user_id, "mode": mode})
        resp.raise_for_status()
        return resp.json()


backend_client = BackendClient()
