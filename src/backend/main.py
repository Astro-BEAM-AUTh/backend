from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Body, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from backend.configs.config import settings
from backend.configs.custom_logging import setup_logger
from backend.database import close_database_connection, create_db_and_tables, initialize_database_connection
from backend.models import StatusResponse
from backend.routers import telescope, web

logger = setup_logger("astro_backend")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """
    Lifecycle manager for the FastAPI application.

    Handles startup and shutdown events.
    """
    logger.info("Starting up the Astro BEAM Backend application...")
    # Perform startup tasks here

    try:
        initialize_database_connection()

        if settings.create_tables_on_startup:
            await create_db_and_tables()

        # TODO @dyka3773: Initialize Kafka producer and consumer when implemented  # noqa: FIX002
        # await initialize_kafka_producer()  # noqa: ERA001
        # await initialize_kafka_consumer()  # noqa: ERA001
        logger.info("All services initialized successfully")
    except Exception:
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
    except Exception:
        logger.exception("Error during shutdown")


app = FastAPI(
    title="Astro BEAM Backend API",
    version=settings.app_version,
    description="Backend API for the Astro BEAM project",
    lifespan=lifespan,
)

app.docs_url = "/docs" if settings.debug else None
app.redoc_url = "/redoc" if settings.debug else None

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="jinja_templates")  # Do not rename this directory to "templates", used in CHANGELOG generation

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


@app.get(
    "/",
    description="Root endpoint providing basic API information.",
    responses={
        200: {"description": "API information retrieved successfully"},
    },
)
async def root() -> Annotated[
    StatusResponse,
    Body(
        examples=[
            {
                "status": "success",
                "message": "Welcome to Astro BEAM Backend API",
                "data": {
                    "version": "1.0.0",
                    "docs_url": "/docs",
                    "redoc_url": "/redoc",
                },
            },
        ],
    ),
]:
    """
    Root endpoint.

    Returns:
        StatusResponse: Welcome message and API info
    """
    return StatusResponse(
        status="success",
        message="Welcome to Astro BEAM Backend API",
        data={
            "version": settings.app_version,
            "docs_url": "/docs" if settings.debug else None,
            "redoc_url": "/redoc" if settings.debug else None,
        },
    )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """Serve the favicon.ico file."""
    return FileResponse("static/favicon.ico")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException) -> JSONResponse | _TemplateResponse:
    message = exception.detail if exception.detail else "An error occurred. Please check your request and try again."

    if request.url.path.startswith("/v1"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",  # TODO @dyka3773: Create a dedicated validation error template # noqa: FIX002
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError) -> JSONResponse | _TemplateResponse:
    if request.url.path.startswith("/v1"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",  # TODO @dyka3773: Create a dedicated validation error template # noqa: FIX002
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


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
