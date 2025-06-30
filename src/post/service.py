from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from ..category.service import CategoryService, get_CategoryService
from ..common.exceptions.conflict import ConflictException
from ..common.exceptions.internal import InternalException
from ..common.exceptions.not_found import NotFoundException
from ..tag.service import TagService, get_TagService
from .models import Post
from .repository import PostRepository, get_PostRepository
from .schemas import CreatePost, UpdatePost


class PostService:
    def __init__(
        self,
        repo: PostRepository,
        category_service: CategoryService,
        tag_service: TagService,
    ):
        self.repository = repo
        self.category_service = category_service
        self.tag_service = tag_service

    async def create_post(self, data: CreatePost, session: AsyncSession) -> Post:
        categories = []
        for category_id in data.category_ids or []:
            category = await self.category_service.get_category_by_id(
                category_id, session
            )
            categories.append(category)
        tags = []
        for tag_id in data.tag_ids or []:
            tag = await self.tag_service.get_tag_by_id(tag_id, session)
            tags.append(tag)

        try:
            post_record = await self.repository.create(
                {**data.model_dump(), "categories": categories, "tags": tags}, session
            )
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
        categories = None
        tags = None
        if update_data.category_ids is not None:
            categories = []
            for category_id in update_data.category_ids:
                category = await self.category_service.get_category_by_id(
                    category_id, session
                )
                categories.append(category)
            post_data["categories"] = categories
        if update_data.tag_ids is not None:
            tags = []
            for tag_id in update_data.tag_ids:
                tag = await self.tag_service.get_tag_by_id(tag_id, session)
                tags.append(tag)
            post_data["tags"] = tags
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
    category_service: Annotated[CategoryService, Depends(get_CategoryService)],
    tag_service: Annotated[TagService, Depends(get_TagService)],
) -> PostService:
    return PostService(postRepository, category_service, tag_service)
