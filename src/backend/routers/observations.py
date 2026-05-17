"""Telescope router for receiving observation requests."""

import logging
import uuid
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.configs.config import settings
from backend.database import get_db
from backend.models import Observation, ObservationRead, ObservationSubmissionRequest
from backend.models.enums.observation_status import ObservationStatus
from backend.utils.auth import (
    AuthPrincipal,
    get_optional_principal,
    get_or_create_guest_user,
    get_or_create_local_user_from_principal,
)
from backend.utils.email.service import send_observation_confirmation_email
from backend.utils.time_utils import utc_now

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy import Result

    from backend.models.user import User

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
    payload: ObservationSubmissionRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    principal: Annotated[AuthPrincipal | None, Depends(get_optional_principal)],
) -> ObservationRead:
    """
    Submit a new telescope observation request.

    Args:
        payload: Observation submission details, consisting of observation parameters and optional requestor information for guest users.
        db: Database session dependency
        principal: Optional authenticated user information from Supabase JWT

    Returns:
        ObservationRead: Confirmation with observation ID and status

    Raises:
        HTTPException: If submission fails
    """
    try:
        if principal is not None:
            user: User = await get_or_create_local_user_from_principal(db, principal)
        else:
            if not payload.requestor:
                logger.warning("Unauthorized attempt to submit observation without authentication or requestor information")
                raise HTTPException(  # noqa: TRY301
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication is required to submit an observation",
                )

            user = await get_or_create_guest_user(db, payload.requestor)

        # Generate unique observation ID
        observation_id = f"obs_{utc_now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"

        # Create observation record
        db_observation = Observation(
            observation_id=observation_id,
            user_id=user.id,
            target_name=payload.observation.target_name,
            observation_object=payload.observation.observation_object,
            ra=payload.observation.ra,
            dec=payload.observation.dec,
            center_frequency=payload.observation.center_frequency,
            rf_gain=payload.observation.rf_gain,
            if_gain=payload.observation.if_gain,
            bb_gain=payload.observation.bb_gain,
            observation_type=payload.observation.observation_type,
            integration_time=payload.observation.integration_time,
            output_filename=payload.observation.output_filename,
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
            payload.observation.observation_object,
            user.username,
        )

        # Send confirmation email to user
        # TODO @dyka3773: Make this a background task so we don't block the request on email sending  # noqa: FIX002
        await send_observation_confirmation_email(db_observation, user)
    except HTTPException:
        raise
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
async def list_observations(
    db: Annotated[AsyncSession, Depends(get_db)],
    principal: Annotated[AuthPrincipal | None, Depends(get_optional_principal)],
) -> list[ObservationRead]:
    """
    Get a list of all telescope observations for the authenticated user.

    Args:
        db: Database session dependency
        principal: Optional authenticated user information from Supabase JWT

    Returns:
        List[ObservationRead]: List of observations

    Raises:
        HTTPException: If user is not authenticated
    """
    try:
        observation_query = select(Observation)

        if principal is not None:
            user = await get_or_create_local_user_from_principal(db, principal)
            observation_query = observation_query.where(Observation.user_id == user.id)
        elif not settings.debug_allow_guest_history:
            logger.warning("Unauthorized attempt to list observations without authentication")
            raise HTTPException(  # noqa: TRY301
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication is required",
            )

        observation_list: Result[tuple[Observation]] = await db.execute(observation_query.order_by(Observation.submitted_at.desc()))
        observations: Sequence[Observation] = observation_list.scalars().all()
    except HTTPException:
        raise
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
async def get_observation(
    observation_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    principal: Annotated[AuthPrincipal | None, Depends(get_optional_principal)],
) -> ObservationRead:
    """
    Get details of a specific telescope observation by ID.

    Args:
        observation_id: ID of the observation to retrieve
        db: Database session dependency
        principal: Optional authenticated user information from Supabase JWT

    Returns:
        ObservationRead: Details of the requested observation

    Raises:
        HTTPException: If observation not found
    """
    # TODO @dyka3773: Refactor to only fetch the requested observation if the user is authenticated and it belongs to them or is made by a guest  # noqa: FIX002
    #                 To do that we can filter using the user_id from the principal or if the user it belongs to has auth_provider='guest'
    result = await db.execute(select(Observation).where(Observation.observation_id == observation_id))
    observation = result.scalar_one_or_none()
    if observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation not found",
        )

    if principal is not None:
        user = await get_or_create_local_user_from_principal(db, principal)
        if observation.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Observation not found",
            )
    elif not settings.debug_allow_guest_history:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication is required",
        )

    return ObservationRead.model_validate(observation).model_dump()


@router.delete(
    "/{observation_id}",
    description="Cancel a pending telescope observation request.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Observation cancelled successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Observation not found"},
    },
)
async def cancel_observation(
    observation_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    principal: Annotated[AuthPrincipal | None, Depends(get_optional_principal)],
) -> None:
    """
    Cancel a pending observation.

    Args:
        observation_id: ID of the observation to cancel
        db: Database session dependency
        principal: Optional authenticated user information from Supabase JWT

    Raises:
        HTTPException: If observation not found or cannot be cancelled
    """
    # TODO @dyka3773: Refactor to only allow cancellation if the user is authenticated and it belongs to them or is made by a guest  # noqa: FIX002
    #                 To do that we can filter using the user_id from the principal or if the user it belongs to has auth_provider='guest'
    result = await db.execute(select(Observation).where(Observation.observation_id == observation_id))
    observation = result.scalar_one_or_none()
    if observation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation not found",
        )

    if principal is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication is required",
        )

    user = await get_or_create_local_user_from_principal(db, principal)

    if observation.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Observation not found",
        )

    if observation.status != ObservationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending observations can be cancelled",
        )

    observation.status = ObservationStatus.CANCELLED
    observation.completed_at = utc_now()
    db.add(observation)
    await db.commit()
    logger.info("Cancelled observation request: %s", observation_id)
