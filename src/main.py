import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .auth.router import router as auth_router
from .category.router import router as category_router
from .comment.router import router as comment_router
from .common.db import create_db_and_tables
from .common.exceptions.register_exceptions import register_exceptions
from .configure_logging import configure_logging
from .file.router import router as file_router
from .post.router import router as post_router
from .tag.router import router as tag_router

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

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(category_router)
app.include_router(tag_router)
app.include_router(file_router)
app.include_router(comment_router)
