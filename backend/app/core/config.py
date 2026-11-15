from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TxnVeyra API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./txnveyra_dev.db"
    backend_cors_origins: list[str] = ["http://localhost:5173"]
    max_upload_size_mb: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("max_upload_size_mb")
    @classmethod
    def validate_upload_limit(cls, value: int) -> int:
        if value < 1 or value > 1024:
            raise ValueError("MAX_UPLOAD_SIZE_MB must be between 1 and 1024")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
