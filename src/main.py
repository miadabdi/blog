import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI

from .auth.router import router as auth_router
from .category.router import router as category_router
from .comment.router import router as comment_router
from .common.db import create_db_and_tables
from .common.exceptions.register_exceptions import register_exceptions
from .common.settings import settings
from .configure_logging import configure_logging
from .file.router import router as file_router
from .post.router import router as post_router
from .tag.router import router as tag_router

if settings.PYTHON_ENV == "development":
    # Enable debug mode for asyncio if DEBUG is True
    import asyncio

    # Set the asyncio event loop to debug mode
    # This will help in debugging issues related to async code
    asyncio.get_event_loop().set_debug(True)

configure_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan_with_db_cleanup(app: FastAPI):
    # Startup
    logger.info("Starting up...")
    await create_db_and_tables()

    yield

    # Shutdown - Database specific cleanup
    logger.info("Cleaning up database connections...")

    # If using SQLAlchemy async engine
    from .common.db import async_engine

    try:
        # Close all database connections
        await async_engine.dispose()
        logger.info("Database engine disposed")
    except Exception as e:
        logger.error(f"Error disposing database engine: {e}")


app = FastAPI(lifespan=lifespan_with_db_cleanup)

register_exceptions(app)


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return {
        "status": "ok",
        "message": "Service is running",
        "current_date": datetime.now(timezone.utc),
    }


app.include_router(auth_router)
app.include_router(post_router)
app.include_router(category_router)
app.include_router(tag_router)
app.include_router(file_router)
app.include_router(comment_router)
