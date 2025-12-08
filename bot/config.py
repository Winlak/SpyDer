from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    bot_token: str
    backend_api_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_prefix="", env_file="/workspace/SpyDer/env/.env")


settings = BotSettings()  # type: ignore
