from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class UserbotSettings(BaseSettings):
    api_id: int
    api_hash: str
    session_string: str | None = None
    backend_api_url: str = "http://localhost:8000"
    owner_telegram_id: int

    model_config = SettingsConfigDict(env_prefix="USERBOT_", env_file="/workspace/SpyDer/env/.env")


settings = UserbotSettings()  # type: ignore
