"""Telescope router for receiving observation requests."""

import logging
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status

from backend.schemas import ApplicationUser, TelescopeObservationRequest, TelescopeObservationResponse

router = APIRouter(
    prefix="/telescope",
    tags=["Telescope"],
)

logger = logging.getLogger("astro_backend")


@router.post(
    "/observations",
    description="Submit a new telescope observation request.",
    responses={
        202: {"description": "Observation request accepted"},
        400: {"description": "Bad Request"},
        503: {"description": "Telescope service unavailable"},
    },
)
async def submit_observation(
    observation: TelescopeObservationRequest,
    requestor: ApplicationUser,
) -> TelescopeObservationResponse:
    """
    Submit a new telescope observation request.

    Args:
        observation: Telescope observation request data
        requestor: Information about the user making the request

    Returns:
        TelescopeObservationResponse: Confirmation with observation ID and status

    Raises:
        HTTPException: If submission fails
    """
    # TODO @dyka3773: Persist the user info and link to observation in DB  # noqa: FIX002
    try:
        # Generate unique observation ID
        observation_id = f"obs_{datetime.now(UTC).strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
        submitted_at = datetime.now(UTC)

        observation.set_id(observation_id)
        observation.set_submission_time(submitted_at)
        observation.set_requestor(requestor.user_id)

        # Send to Kafka for processing
        # TODO @dyka3773: Implement actual Kafka sending logic  # noqa: FIX002
        # await send_telescope_observation_request(observation) # noqa: ERA001

        # TODO @dyka3773: Persist the observation request in the database  # noqa: FIX002

        logger.info(
            "Submitted observation request: %s for target %s",
            observation_id,
            observation.observation_object,
        )

        return TelescopeObservationResponse(
            observation_id=observation_id,
            status="pending",
            submitted_at=submitted_at,
            message="Observation request submitted successfully",
        )

    except Exception as e:
        logger.exception("Failed to submit observation request")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to submit observation: {e!s}",
        ) from e


@router.delete(
    "/observations/{observation_id}",
    description="Cancel a pending telescope observation request.",
    responses={
        204: {"description": "Observation cancelled successfully"},
        404: {"description": "Observation not found"},
    },
)
async def cancel_observation(observation_id: str) -> None:
    """
    Cancel a pending observation.

    Args:
        observation_id: ID of the observation to cancel

    Raises:
        HTTPException: If observation not found or cannot be cancelled
    """
    # TODO @dyka3773: Implement actual cancellation logic with database  # noqa: FIX002
    # For now, we mock the behavior
    if not observation_id.startswith("obs_"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation not found",
        )
    logger.info("Cancelled observation request: %s", observation_id)
