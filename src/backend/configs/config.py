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

    # Supabase authentication settings
    supabase_url: str = Field(
        default="",
        description="Supabase project URL, for example https://<project-ref>.supabase.co",
    )
    supabase_audience: str = Field(
        default="authenticated",
        description="Expected JWT audience",
    )
    supabase_allowed_jwt_algorithms: list[str] = Field(
        default=["RS256"],
        description="Allowed JWT signing algorithms for Supabase token verification",
    )
    auth_required: bool = Field(
        default=True,
        description="Require a verified Supabase JWT for protected endpoints",
    )
    debug_allow_guest_history: bool = Field(
        default=False,
        description="Allow guest observation history access in debug mode",
    )

    # Email settings
    smtp_server: str = Field(
        default="smtp.gmail.com",
        description="SMTP server hostname",
    )
    smtp_port: int = Field(
        default=587,
        description="SMTP server port",
    )
    smtp_username: str = Field(
        default="",
        description="SMTP authentication username",
    )
    smtp_password: str = Field(
        default="",
        description="SMTP authentication password",
    )
    smtp_sender_email: str = Field(
        default="noreply@astrobeam.example.com",
        description="Email address to send from",
    )
    smtp_use_tls: bool = Field(
        default=True,
        description="Use TLS for SMTP connection",
    )

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

    @property
    def supabase_issuer_url(self) -> str:
        """Return the expected JWT issuer URL."""
        if not self.supabase_url:
            return ""

        return f"{self.supabase_url.rstrip('/')}/auth/v1"

    @property
    def supabase_jwks_endpoint(self) -> str:
        """Return the JWKS endpoint used for token verification."""
        issuer = self.supabase_issuer_url
        if not issuer:
            return ""

        return f"{issuer}/.well-known/jwks.json"


# Global settings instance
settings = Settings()
