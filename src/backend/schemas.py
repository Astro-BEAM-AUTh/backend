"""Pydantic models for API requests and responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


# Telescope observation models
class TelescopeObservationRequest(BaseModel):
    """Request model for telescope observations."""

    target_name: str = Field(..., description="Name of the observation target")
    center_frequency: float = Field(..., description="Center frequency in MHz")
    rf_gain: float = Field(..., description="RF gain in dB")
    if_gain: float = Field(..., description="IF gain in dB")
    bb_gain: float = Field(..., description="Baseband gain in dB")
    # TODO @kesoglidis: What are the possible observation types?  # noqa: FIX002
    # TODO @dyka3773: Reintroduce ObservationTypeEnum when implemented  # noqa: FIX002
    # observation_type: ObservationTypeEnum = Field( ..., description="Type of observation" ) # noqa: ERA001
    observation_type: str = Field(..., description="Type of observation")
    integration_time: float = Field(..., description="Integration time in seconds")
    observation_object: str = Field(..., description="Object being observed")
    ra: float = Field(..., description="Right Ascension in degrees")
    dec: float = Field(..., description="Declination in degrees")
    output_filename: str = Field(..., description="Filename for the observation data")

    model_config = {
        "json_schema_extra": {
            "example": {
                "target_name": "M31",
                "center_frequency": 1400.0,
                "rf_gain": 30.0,
                "if_gain": 20.0,
                "bb_gain": 10.0,
                "observation_type": "imaging",
                "integration_time": 600.0,
                "observation_object": "Andromeda Galaxy",
                "ra": 10.68470833,
                "dec": 41.26875,
                "output_filename": "m31_observation.fits",
            },
        },
    }


class TelescopeObservationResponse(BaseModel):
    """Response model for telescope observations."""

    observation_id: str = Field(..., description="Unique observation identifier")
    status: str = Field(..., description="Current observation status")
    submitted_at: datetime = Field(..., description="Timestamp of submission")
    message: str = Field(..., description="Response message")

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Observation request submitted successfully",
                "observation_id": "obs_20231110_001",
                "status": "pending",
                "submitted_at": "2023-11-10T12:34:56Z",
            }
        }
    }


# Web/UI data models
class StatusResponse(BaseModel):
    """Generic status response."""

    status: str = Field(..., description="Status indicator")
    message: str | None = Field(None, description="Optional message")
    data: dict[str, Any] | None = Field(None, description="Optional data payload")

    model_config = {
        "json_schema_extra": {
            "example": {
                "data": {
                    "active_observations": 3,
                    "uptime": 86400,
                },
                "message": "System is operational",
                "status": "healthy",
            },
        },
    }


class ApplicationUser(BaseModel):
    """Model representing an application user."""

    user_id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., description="Username of the application user")
    email: EmailStr = Field(..., description="Email address of the user")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "user_12345",
                "username": "astro_user",
                "email": "astro_user@example.com",
            },
        },
    }
