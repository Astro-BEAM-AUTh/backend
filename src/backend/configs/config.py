"""Application configuration using Pydantic Settings."""

from importlib import metadata

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application settings
    app_name: str = Field(default="Astro BEAM Backend", description="Application name")
    app_version: str = Field(default=metadata.version("backend"), description="Application version")
    environment: str = Field(default="DEV", description="Application environment")
    debug: bool = Field(default=True, description="Debug mode")  # Only for DEV
    host: str = Field(default="127.0.0.1", description="Host to bind to")
    port: int = Field(default=8000, description="Port to bind to")

    # Database settings
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/astro_beam",
        description="PostgreSQL database URL",
    )
    db_echo: bool = Field(default=True, description="Echo SQL queries")  # Only for DEV

    # Kafka settings
    kafka_bootstrap_servers: str = Field(
        default="localhost:9092",
        description="Kafka bootstrap servers",
    )
    # TODO @dyka3773: Add more Kafka settings as needed  # noqa: FIX002

    # CORS settings
    cors_origins: list[str] = Field(
        default=[
            "http://localhost:4200",  # Angular frontend default origin
        ],
        description="Allowed CORS origins",
    )
    cors_allow_credentials: bool = Field(
        default=True,
        description="Allow CORS credentials",
    )
    cors_allow_methods: list[str] = Field(
        default=["*"],
        description="Allowed CORS methods",
    )
    cors_allow_headers: list[str] = Field(
        default=["*"],
        description="Allowed CORS headers",
    )


# Global settings instance
settings = Settings()
