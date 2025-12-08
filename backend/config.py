from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendSettings(BaseSettings):
    database_url: str
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0

    model_config = SettingsConfigDict(env_prefix="", env_file="/workspace/SpyDer/env/.env")


settings = BackendSettings()  # type: ignore
