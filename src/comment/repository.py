from functools import lru_cache

from sqlmodel import select

from ..common.generic_repository import GenericRepository
from .models import Comment


class CommentRepository(GenericRepository[Comment]):
    def __init__(self):
        super().__init__(Comment)

    async def get_by_post_id(self, post_id: int, session):
        result = await session.exec(
            select(self.model).where(self.model.post_id == post_id)
        )
        return list(result)


@lru_cache
def get_CommentRepository():
    return CommentRepository()
