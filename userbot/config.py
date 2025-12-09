from __future__ import annotations

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class UserbotSettings(BaseSettings):
    api_id: int = Field(alias="USERBOT_API_ID")
    api_hash: str = Field(alias="USERBOT_API_HASH")
    session_string: str | None = Field(default=None, alias="USERBOT_SESSION_STRING")
    backend_api_url: AnyHttpUrl | str = Field(default="http://backend:8000", alias="BACKEND_API_URL")
    owner_telegram_id: int = Field(alias="USERBOT_OWNER_TELEGRAM_ID")

    model_config = SettingsConfigDict(env_prefix="", env_file="env/.env", extra="ignore")


settings = UserbotSettings()  # type: ignore
