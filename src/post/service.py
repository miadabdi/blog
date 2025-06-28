from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Post
from .repository import PostRepository, get_PostRepository
from .schemas import CreatePost, UpdatePost


class PostService:
    def __init__(self, repo: PostRepository):
        self.repository = repo

    async def create_post(self, data: CreatePost, session: AsyncSession) -> Post:
        post_record = await self.repository.create(data.model_dump(), session)
        await session.commit()
        return post_record

    async def update_post(
        self, id: int, update_data: UpdatePost, session: AsyncSession
    ) -> Post:
        post_data = update_data.model_dump(exclude_unset=True)
        updated_post = await self.repository.update(id, post_data, session)
        await session.commit()
        return updated_post

    async def delete_post(self, id: int, session: AsyncSession) -> Post:
        result = await self.repository.delete(id, session)
        await session.commit()
        return result

    async def get_post_by_id(self, id: int, session: AsyncSession) -> Post:
        result = await self.repository.get_by_id(id, session)
        await session.commit()

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} not found",
            )

        return result


@lru_cache
def get_PostService(
    postRepository: Annotated[PostRepository, Depends(get_PostRepository)],
) -> PostService:
    return PostService(postRepository)
