"""
Repository layer for Comment.
Handles direct database operations for Comment entities.
"""

from functools import lru_cache

from sqlmodel import select

from ..common.generic_repository import GenericRepository
from .models import Comment


class CommentRepository(GenericRepository[Comment]):
    """
    Repository for Comment model, inherits generic CRUD operations.
    """

    def __init__(self):
        super().__init__(Comment)

    async def get_by_post_id(self, post_id: int, session):
        """
        Retrieve all comments for a given post ID.

        Args:
            post_id (int): The ID of the post.
            session: Database session.

        Returns:
            list[Comment]: List of comments for the post.
        """
        result = await session.exec(
            select(self.model).where(self.model.post_id == post_id)
        )
        return list(result)


@lru_cache
def get_CommentRepository():
    """
    Dependency injector for CommentRepository.
    """
    return CommentRepository()
