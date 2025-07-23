"""
Database engine and session management for SQLModel and SQLAlchemy.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .settings import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    echo_pool=False,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=True,
    expire_on_commit=False,
    bind=async_engine,
    class_=AsyncSession,
)


async def create_db_and_tables():
    """
    Create all tables in the database.
    """
    async with async_engine.begin() as conn:
        # For SQLModel, this will create the tables (but won't drop existing ones)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """
    Dependency for getting an async database session.

    Yields:
        AsyncSession: The database session.
    """
    async with SessionLocal.begin() as session:
        yield session
