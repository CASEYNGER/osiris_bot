"""Конфигурационные настройки."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    """Настройки."""

    bot_token: SecretStr
    admin: int
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
        )


config = Settings()
