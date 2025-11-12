"""Response models for API endpoints."""

from typing import Any

from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    """Generic status response for health checks and system status."""

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
