from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Blog"

    POSTGRES_HOST: str = Field(min_length=1)
    POSTGRES_PORT: int = Field(gt=1, lt=65536)
    POSTGRES_DB: str = Field(min_length=1)
    POSTGRES_USER: str = Field(min_length=1)
    POSTGRES_PASSWORD: str = Field(min_length=1)

    SECRET_KEY: str = Field(min_length=12)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(ge=10)

    MINIO_SECURE: bool = Field(default=False)
    MINIO_ENDPOINT: str = Field(min_length=1)
    MINIO_PORT: int = Field(gt=0, lt=65536)
    MINIO_ACCESS_KEY: str = Field(min_length=1)
    MINIO_SECRET_KEY: str = Field(min_length=1)
    MINIO_BUCKET_NAMES: list[str] = ["images", "files"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings():
    return Settings.model_validate({})


settings = get_settings()
