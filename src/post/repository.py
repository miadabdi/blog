from functools import lru_cache

from ..common.generic_repository import GenericRepository
from .models import Post


class PostRepository(GenericRepository[Post]):
    def __init__(self):
        print("POST REPO CREATED")
        super().__init__(Post)

    async def update_with_m2m(
        self,
        post,
        post_data,
        session,
        categories=None,
        tags=None,
    ):
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
    return PostRepository()
