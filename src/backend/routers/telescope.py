"""Telescope router for receiving observation requests."""

import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.database import get_db
from backend.models import Observation, ObservationCreate, ObservationRead, User, UserCreate
from backend.utils.time_utils import utc_now

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
    observation: ObservationCreate,
    requestor: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ObservationRead:
    """
    Submit a new telescope observation request.

    Args:
        observation(ObservationCreate): Telescope observation request data
        requestor(UserCreate): Information about the user making the request
        db(AsyncSession): Database session

    Returns:
        ObservationRead: Confirmation with observation ID and status

    Raises:
        HTTPException: If submission fails
    """
    try:
        # Get or create user
        result = await db.execute(select(User).where(User.user_id == requestor.user_id))
        user = result.scalar_one_or_none()

        if user is None:
            # Create new user
            user = User(
                user_id=requestor.user_id,
                username=requestor.username,
                email=requestor.email,
            )
            db.add(user)
            await db.flush()  # Flush to get the user.id

        # Generate unique observation ID
        observation_id = f"obs_{utc_now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"

        # Create observation record
        db_observation = Observation(
            observation_id=observation_id,
            user_id=user.id,
            target_name=observation.target_name,
            observation_object=observation.observation_object,
            ra=observation.ra,
            dec=observation.dec,
            center_frequency=observation.center_frequency,
            rf_gain=observation.rf_gain,
            if_gain=observation.if_gain,
            bb_gain=observation.bb_gain,
            observation_type=observation.observation_type,
            integration_time=observation.integration_time,
            output_filename=observation.output_filename,
            status="pending",
            submitted_at=utc_now(),
        )

        # Send to Kafka for processing
        # TODO @dyka3773: Implement actual Kafka sending logic  # noqa: FIX002
        # await send_telescope_observation_request(db_observation) # noqa: ERA001

        # Persist observation in database
        db.add(db_observation)
        await db.commit()
        await db.refresh(db_observation)

        logger.info(
            "Submitted observation request: %s for target %s by user %s",
            observation_id,
            observation.observation_object,
            user.username,
        )
    except Exception as e:
        logger.exception("Failed to submit observation request")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to submit observation: {e!s}",
        ) from e
    else:
        # Convert database model to read schema
        return ObservationRead.model_validate(db_observation)


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
