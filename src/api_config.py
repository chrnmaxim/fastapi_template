from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from src import api_constants

__all__ = ["api_settings"]


class ApiSettings(BaseSettings):
    """Base class for API environment variables and settings."""

    # App
    MODE: Literal["PROD", "DEV", "LOCAL", "TEST"]
    APP_NAME: str = "app"
    APP_VERSION: str = "0.1.0"

    # Security
    CORS_ORIGINS: list[str] = ["*"]

    # Postgres
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POOL_SIZE: int
    MAX_OVERFLOW: int

    @property
    def DATABASE_URL(self) -> str:
        """PostgreSQL database URL."""

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=api_constants.ENV_PATH, extra="allow")


api_settings: ApiSettings = ApiSettings()  # type: ignore
