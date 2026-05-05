"""Background-style tool that processes pending observations one by one."""

import asyncio

from sqlmodel import select

from backend.configs.custom_logging import setup_logger
from backend.database import close_database_connection, get_db_session, initialize_database_connection
from backend.models import Observation
from backend.models.enums.observation_status import ObservationStatus
from backend.utils.time_utils import utc_now

PROCESS_DELAY_SECONDS = 5
POLL_DELAY_SECONDS = 10

logger = setup_logger("observation_processor")


async def claim_next_pending_observation() -> Observation | None:
    """Fetch and claim one pending observation for processing."""
    async with get_db_session() as session:
        result = await session.execute(
            select(Observation).where(Observation.status == ObservationStatus.PENDING.value).order_by(Observation.submitted_at.asc()).limit(1),
        )
        observation = result.scalar_one_or_none()

        if observation is None:
            return None

        observation.status = ObservationStatus.IN_PROGRESS.value
        observation.updated_at = utc_now()

        logger.info("Claimed observation %s for processing", observation.observation_id)

        await session.flush()
        await session.refresh(observation)
        return observation


async def mark_observation_completed(observation_id: int) -> None:
    """Mark an observation as completed after successful processing."""
    async with get_db_session() as session:
        observation = await session.get(Observation, observation_id)
        if observation is None:
            logger.warning("Observation with database id %s no longer exists", observation_id)
            return

        observation.status = ObservationStatus.COMPLETED.value
        observation.completed_at = utc_now()
        observation.updated_at = utc_now()

        logger.info("Marked observation %s as completed", observation_id)


async def mark_observation_failed(observation_id: int) -> None:
    """Mark an observation as failed when processing raises an exception."""
    async with get_db_session() as session:
        observation = await session.get(Observation, observation_id)
        if observation is None:
            logger.warning("Observation with database id %s no longer exists", observation_id)
            return

        observation.status = ObservationStatus.FAILED.value
        observation.updated_at = utc_now()


async def process_observation(observation: Observation) -> None:
    """Simulate processing of an observation using a fixed delay."""
    logger.info(
        "Processing observation %s (%s)",
        observation.observation_id,
        observation.target_name,
    )

    await asyncio.sleep(PROCESS_DELAY_SECONDS)
    await mark_observation_completed(observation.id)

    logger.info("Completed observation %s", observation.observation_id)


async def run_processor() -> None:
    """Run the worker loop that processes pending observations and polls for new ones."""
    logger.info(
        "Starting observation processor (process delay: %ss, poll delay: %ss)",
        PROCESS_DELAY_SECONDS,
        POLL_DELAY_SECONDS,
    )

    initialize_database_connection()

    try:
        while True:
            observation = await claim_next_pending_observation()
            if observation is None:
                logger.info("No pending observations found; polling again in %s seconds", POLL_DELAY_SECONDS)
                await asyncio.sleep(POLL_DELAY_SECONDS)
                continue

            try:
                await process_observation(observation)
            except Exception:
                logger.exception("Observation processing failed for %s", observation.observation_id)
                await mark_observation_failed(observation.id)
    finally:
        await close_database_connection()
        logger.info("Observation processor stopped")


def main() -> None:
    """Entry point for the observation processor tool."""
    try:
        asyncio.run(run_processor())
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down processor")


if __name__ == "__main__":
    main()
