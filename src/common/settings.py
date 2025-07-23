"""
Application settings and configuration using Pydantic BaseSettings.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the application, loaded from environment variables or .env file.

    Attributes:
        app_name (str): Name of the application.
        PYTHON_ENV (str): Environment type.
        POSTGRES_HOST (str): PostgreSQL host.
        POSTGRES_PORT (int): PostgreSQL port.
        POSTGRES_DB (str): PostgreSQL database name.
        POSTGRES_USER (str): PostgreSQL user.
        POSTGRES_PASSWORD (str): PostgreSQL password.
        SECRET_KEY (str): Secret key for JWT.
        ALGORITHM (str): JWT algorithm.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): JWT token expiry.
        MINIO_SECURE (bool): Use HTTPS for MinIO.
        MINIO_ENDPOINT (str): MinIO endpoint.
        MINIO_PORT (int): MinIO port.
        MINIO_ACCESS_KEY (str): MinIO access key.
        MINIO_SECRET_KEY (str): MinIO secret key.
        MINIO_BUCKET_NAMES (list[str]): List of MinIO bucket names.
    """

    app_name: str = "Blog"

    PYTHON_ENV: str = Field(
        default="development",
        description="Environment for the Python application (development, production, etc.)",
    )

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
    """
    Get the cached Settings instance.

    Returns:
        Settings: The application settings.
    """
    return Settings.model_validate({})


settings = get_settings()
