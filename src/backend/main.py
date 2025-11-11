from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.configs.config import settings
from backend.configs.custom_logging import setup_logger
from backend.database import close_database_connection, initialize_database_connection
from backend.routers import telescope, web

logger = setup_logger("astro_backend")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    Lifecycle manager for the FastAPI application.

    Handles startup and shutdown events.
    """
    logger.info("Starting up the Astro BEAM Backend application...")
    # Perform startup tasks here

    try:
        initialize_database_connection()

        # TODO @dyka3773: Initialize Kafka producer and consumer when implemented  # noqa: FIX002
        # await initialize_kafka_producer()  # noqa: ERA001
        # await initialize_kafka_consumer()  # noqa: ERA001
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.exception("Failed to initialize services")
        raise

    yield

    logger.info("Shutting down the Astro BEAM Backend application...")
    # Perform shutdown tasks here
    try:
        # TODO @dyka3773: Close Kafka producer and consumer when implemented  # noqa: FIX002
        # await close_kafka_producer()  # noqa: ERA001
        # await close_kafka_consumer()  # noqa: ERA001
        await close_database_connection()
        logger.info("All services closed successfully")
    except Exception as e:
        logger.exception("Error during shutdown")


app = FastAPI(
    title="Astro BEAM Backend API",
    version=settings.app_version,
    description="Backend API for the Astro BEAM project",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.include_router(
    telescope.router,
    prefix="/v1",
)
app.include_router(
    web.router,
    prefix="/v1",
)


@app.get("/")
async def root() -> dict:
    """
    Root endpoint.

    Returns:
        dict: Welcome message and API info
    """
    return {
        "message": "Welcome to Astro BEAM Backend API",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.debug else None,
        "redoc_url": "/redoc" if settings.debug else None,
    }


def main() -> None:
    """Entry point for running the Astro BEAM Backend application using Uvicorn."""
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
