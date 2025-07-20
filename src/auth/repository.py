from functools import lru_cache
from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..common.generic_repository import GenericRepository
from .models import User


class UserRepository(GenericRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        """Get a record by Email"""
        return (
            await session.exec(select(self.model).where(self.model.email == email))
        ).first()


@lru_cache
def get_UserRepository():
    return UserRepository()
