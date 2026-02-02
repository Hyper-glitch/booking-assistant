from logging import INFO
from pathlib import Path
from typing import Any, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(".env"),
        env_file_encoding="utf-8",
    )

    DEBUG: bool = False
    LOG_LEVEL: int = INFO
    APP_NAME: str = "booking-assistant"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    APP_ENV: Literal["local", "dev", "prod"] = "local"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    APP_AUTH_TOKEN: str

    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_HOST: str = "database"
    POSTGRESQL_PORT: int = 5432
    POSTGRESQL_DB: str = "database"

    METRICS_URL: str = "/monitoring/metrics"

    LLM_TEMPERATURE: float = 0.0
    LLM_TOP_P: float = 0.7
    LLM_MAX_TOKENS: int = 512
    LLM_SERVER_URL: str
    LLM_MODEL_NAME: str
    LLM_API_KEY: str

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.POSTGRESQL_USERNAME}:{self.POSTGRESQL_PASSWORD}"
            f"@{self.POSTGRESQL_HOST}:{self.POSTGRESQL_PORT}/{self.POSTGRESQL_DB}"
        )

    @property
    def llm_params(self) -> dict[str, Any]:
        return {
            "model": self.LLM_MODEL_NAME,
            "temperature": self.LLM_TEMPERATURE,
            "top_p": self.LLM_TOP_P,
            "max_tokens": self.LLM_MAX_TOKENS,
            "api_key": self.LLM_API_KEY,
            "base_url": self.LLM_SERVER_URL,
        }


settings = Settings()
