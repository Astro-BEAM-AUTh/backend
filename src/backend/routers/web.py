"""Web router for sending data to the UI."""

import logging
from datetime import UTC, datetime

from fastapi import APIRouter, status

from backend.configs.config import settings
from backend.models import StatusResponse

router = APIRouter(
    prefix="/web",
    tags=["Web"],
    responses={
        status.HTTP_200_OK: {"description": "Successful Response"},
    },
)

logger = logging.getLogger("astro_backend")


@router.get(
    "/health",
    description="Health check endpoint for the API.",
    responses={
        status.HTTP_200_OK: {"description": "API is healthy"},
    },
)
async def health_check() -> StatusResponse:
    """
    Health check endpoint for the API.

    Returns:
        StatusResponse: Current health status
    """
    return StatusResponse(
        status="healthy",
        message="API is running",
        data={
            "timestamp": datetime.now(UTC).isoformat(),
            "version": settings.app_version,
        },
    )


@router.get(
    "/status",
    description="Get overall system status including telescope and observation queue info.",
    responses={
        status.HTTP_200_OK: {"description": "System status retrieved successfully"},
    },
)
async def get_system_status() -> StatusResponse:
    """
    Get overall system status including telescope and observation queue info.

    Returns:
        StatusResponse: System status information
    """
    return StatusResponse(
        status="operational",
        message="All systems nominal",
        data={
            # TODO @dyka3773: Replace mock data with real-time system metrics  # noqa: FIX002
            "active_telescopes": 1,
            "observations_today": 42,
            "queue_length": 5,
            "last_updated": datetime.now(UTC).isoformat(),
        },
    )
