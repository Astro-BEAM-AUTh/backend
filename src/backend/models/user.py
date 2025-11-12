"""User database model."""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.models.observation import Observation


class UserBase(SQLModel):
    """Base model for users shared between API and database."""

    user_id: str = Field(description="Unique user identifier")
    username: str = Field(description="Username")
    email: EmailStr = Field(description="Email address")


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
    user_id: str = Field(unique=True, index=True, description="Unique user identifier")
    username: str = Field(unique=True, index=True, description="Username")
    email: str = Field(unique=True, index=True, description="Email address")

    # Relationship to observations
    observations: list["Observation"] = Relationship(back_populates="user")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record update timestamp")
    is_active: bool = Field(default=True, description="Whether the user is active")
