from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from ..common.exceptions.conflict import ConflictException
from ..common.exceptions.internal import InternalException
from ..common.exceptions.not_found import NotFoundException
from .models import Post
from .repository import PostRepository, get_PostRepository
from .schemas import CreatePost, UpdatePost


class PostService:
    def __init__(self, repo: PostRepository):
        self.repository = repo

    async def create_post(self, data: CreatePost, session: AsyncSession) -> Post:
        try:
            post_record = await self.repository.create(data.model_dump(), session)
        except IntegrityError:
            raise ConflictException(
                resource=Post.__name__,
                message="Duplicate title",
            )
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while creating the category.",
                underlying_error=e,
            )

        return post_record

    async def update_post(
        self, id: int, update_data: UpdatePost, session: AsyncSession
    ) -> Post:
        post_data = update_data.model_dump(exclude_unset=True)
        try:
            updated_post = await self.repository.update(id, post_data, session)
        except IntegrityError:
            raise ConflictException(
                resource=Post.__name__,
                message="Duplicate title",
            )
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while creating the category.",
                underlying_error=e,
            )

        return updated_post

    async def delete_post(self, id: int, session: AsyncSession) -> Post:
        result = await self.repository.delete(id, session)
        return result

    async def get_post_by_id(self, id: int, session: AsyncSession) -> Post:
        result = await self.repository.get_by_id(id, session)

        if result is None:
            raise NotFoundException(Post.__name__, str(id))

        return result


@lru_cache
def get_PostService(
    postRepository: Annotated[PostRepository, Depends(get_PostRepository)],
) -> PostService:
    return PostService(postRepository)
