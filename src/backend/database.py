"""Database connection and session management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.configs.config import settings

# Database engine
engine: AsyncEngine | None = None

# Session factory
async_session_maker: async_sessionmaker[AsyncSession] | None = None


def initialize_database_connection() -> None:
    """Initialize database connection and session factory."""
    global engine, async_session_maker  # noqa: PLW0603

    engine = create_async_engine(
        str(settings.database_url),
        echo=settings.db_echo,
        pool_pre_ping=True,
    )

    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def close_database_connection() -> None:
    """Close database connection."""
    if engine is not None:
        await engine.dispose()


async def create_db_and_tables() -> None:
    """
    Create database tables based on SQLModel metadata.

    Note: In production, you should use Alembic migrations instead.
    This is useful for development and testing.
    """
    if engine is None:
        msg = "Database not initialized. Call initialize_database_connection() first."
        raise RuntimeError(msg)

    async with engine.begin() as conn:
        # Import models to register them with SQLModel
        from backend.models import Observation, User  # noqa: F401, PLC0415

        await conn.run_sync(SQLModel.metadata.create_all, tables=[Observation, User])


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """
    Get a database session.

    Yields:
        AsyncSession: Database session

    Usage:
        async with get_db_session() as session:
            result = await session.execute(query)
    """
    if async_session_maker is None:
        msg = "Database not initialized. Call initialize_database_connection() first."
        raise RuntimeError(msg)

    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_db() -> AsyncGenerator[AsyncSession]:
    """
    Dependency for FastAPI routes to get database session.

    Yields:
        AsyncSession: Database session

    Usage:
        @router.get("/")
        async def route(db: AsyncSession = Depends(get_db)):
            result = await db.execute(query)
    """
    async with get_db_session() as session:
        yield session
