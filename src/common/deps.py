"""
Dependency definitions for FastAPI routes.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .db import get_session

# Alias for dependency-injected AsyncSession
AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
