"""
Repository layer for Post.
Handles direct database operations for Post entities.
"""

from functools import lru_cache

from sqlmodel import select

from ..common.generic_repository import GenericRepository
from .models import Post


class PostRepository(GenericRepository[Post]):
    """
    Repository for Post model, inherits generic CRUD operations.
    """

    def __init__(self):
        super().__init__(Post)

    async def get_all(self, session) -> list[Post]:
        """
        Get all posts, newest first.
        """
        return list(
            (
                await session.exec(
                    select(self.model).order_by(self.model.created_at.desc())
                )
            ).all()
        )

    async def get_by_slug(self, slug: str, session) -> Post | None:
        """
        Get a post by its slug.
        """
        return (
            await session.exec(select(self.model).where(self.model.slug == slug))
        ).first()

    async def update_with_m2m(
        self,
        post,
        post_data,
        session,
        categories=None,
        tags=None,
    ):
        """
        Update a post with many-to-many relationships.

        Args:
            post: The post instance to update.
            post_data: Dictionary of fields to update.
            session: Database session.
            categories: List of category instances or None.
            tags: List of tag instances or None.

        Returns:
            Post: The updated post instance.
        """
        # Update scalar fields
        for key, value in post_data.items():
            if key not in ("category_ids", "tag_ids"):
                setattr(post, key, value)

        # Overwrite relations if provided
        if categories is not None:
            post.categories = categories
        if tags is not None:
            post.tags = tags

        session.add(post)
        await session.flush()
        await session.refresh(post)
        return post


@lru_cache
def get_PostRepository():
    """
    Dependency injector for PostRepository.
    """
    return PostRepository()
