"""Telescope router for receiving observation requests."""

import logging
import uuid
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.database import get_db
from backend.models import Observation, ObservationCreate, ObservationRead, User, UserCreate
from backend.models.enums.observation_status import ObservationStatus
from backend.utils.email.service import send_observation_confirmation_email
from backend.utils.time_utils import utc_now

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy import Result

router = APIRouter(
    prefix="/observations",
    tags=["Observation"],
)

logger = logging.getLogger("astro_backend")


@router.post(
    "/",
    description="Submit a new telescope observation request.",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {"description": "Observation request accepted"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Telescope service unavailable"},
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
            status=ObservationStatus.PENDING,
            submitted_at=utc_now(),
        )

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

        # Send confirmation email to user
        await send_observation_confirmation_email(db_observation, user)
    except Exception as e:
        logger.exception("Failed to submit observation request")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to submit observation: {e!s}",
        ) from e
    else:
        # Convert database model to read schema
        return ObservationRead.model_validate(db_observation).model_dump()


@router.get(
    "/",
    description="Get a list of all telescope observations for the authenticated user.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "List of observations retrieved successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def list_observations(db: Annotated[AsyncSession, Depends(get_db)]) -> list[ObservationRead]:
    """
    Get a list of all telescope observations for the authenticated user.

    Returns:
        List[ObservationRead]: List of observations
    Raises:
        HTTPException: If user is not authenticated
    """
    # TODO @dyka3773: Implement actual user authentication and filter observations by user  # noqa: FIX002
    # TODO @dyka3773: Implement pagination for observation list  # noqa: FIX002
    try:
        observation_list: Result[tuple[Observation]] = await db.execute(select(Observation))
        observations: Sequence[Observation] = observation_list.scalars().all()
    except Exception as e:
        logger.exception("Failed to list observations")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to list observations: {e!s}",
        ) from e
    else:
        return [ObservationRead.model_validate(obs).model_dump() for obs in observations]


@router.get(
    "/{observation_id}",
    description="Get details of a specific telescope observation by ID.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Observation details retrieved successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Observation not found"},
    },
)
async def get_observation(observation_id: str) -> ObservationRead:
    """
    Get details of a specific telescope observation by ID.

    Args:
        observation_id: ID of the observation to retrieve

    Returns:
        ObservationRead: Details of the requested observation

    Raises:
        HTTPException: If observation not found
    """
    # TODO @dyka3773: Implement actual retrieval logic with database  # noqa: FIX002
    logger.warning("Not implemented: get_observation for observation_id %s", observation_id)
    # For now, we mock the behavior
    if not observation_id.startswith("obs_"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation not found",
        )
    return ObservationRead(
        observation_id=observation_id,
        user_id=1,
        target_name="Mock Target",
        observation_object="Mock Object",
        ra=123.45,
        dec=-54.32,
        center_frequency=1400.0,
        rf_gain=10.0,
        if_gain=20.0,
        bb_gain=30.0,
        observation_type="imaging",
        integration_time=60,
        output_filename="mock_output.fits",
        status=ObservationStatus.PENDING,
        submitted_at=utc_now(),
    )


@router.delete(
    "/{observation_id}",
    description="Cancel a pending telescope observation request.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Observation cancelled successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Observation not found"},
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
    logger.warning("Not implemented: cancel_observation for observation_id %s", observation_id)
    # For now, we mock the behavior
    if not observation_id.startswith("obs_"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation not found",
        )
    logger.info("Cancelled observation request: %s", observation_id)
