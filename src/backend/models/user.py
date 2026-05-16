"""User database model."""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import event
from sqlmodel import Field, Relationship, SQLModel, String
from sqlmodel._compat import SQLModelConfig

from backend.utils.time_utils import utc_now

if TYPE_CHECKING:
    from backend.models.observation import Observation


class UserBase(SQLModel):
    """Base model for users shared between API and database."""

    user_id: str = Field(description="Unique user identifier")
    username: str = Field(description="Username")
    email: EmailStr = Field(description="Email address")
    auth_provider: str = Field(default="guest", description="Authentication provider")

    model_config: SQLModelConfig = {
        "json_schema_extra": {
            "example": {
                "user_id": "123456",
                "username": "astro_test_user",
                "email": "software@astrobeam.gr",
                "auth_provider": "guest",
            },
        },
    }


class UserCreate(UserBase):
    """Schema for creating a new user (API request)."""


class UserRead(UserBase):
    """Schema for reading a user (API response)."""

    id: int = Field(description="Database primary key")
    is_active: bool = Field(description="Whether the user is active")
    created_at: datetime = Field(description="Record creation timestamp")


class User(UserBase, table=True):
    """Database model for application users."""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(unique=True, index=True, description="Unique user identifier", sa_type=String())
    username: str = Field(index=True, description="Username", sa_type=String())
    email: EmailStr = Field(unique=True, index=True, description="Email address", sa_type=String())
    auth_provider: str = Field(default="guest", index=True, description="Authentication provider", sa_type=String())

    # Relationship to observations
    observations: list["Observation"] = Relationship(back_populates="user")

    # Metadata
    created_at: datetime = Field(default_factory=utc_now, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=utc_now, description="Record update timestamp")
    is_active: bool = Field(default=True, description="Whether the user is active")

    model_config: SQLModelConfig = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": "123456",
                "username": "astro_test_user",
                "email": "software@astrobeam.gr",
                "auth_provider": "guest",
                "is_active": True,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z",
            },
        },
    }

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, user_id='{self.user_id}', username='{self.username}', email='{self.email}', auth_provider='{self.auth_provider}')>"
        )


@event.listens_for(User, "before_update")
def update_updated_at(_: object, __: object, target: User) -> None:
    """Automatically update the 'updated_at' timestamp on record update."""
    target.updated_at = utc_now()
