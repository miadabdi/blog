"""
Service layer for Post operations.
Handles business logic and error handling for post CRUD operations.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from ..auth.models import User
from ..category.service import CategoryService, get_CategoryService
from ..common.exceptions.exceptions import (
    DuplicateEntryException,
    EntityNotFoundException,
    InternalException,
)
from ..tag.service import TagService, get_TagService
from .models import Post
from .repository import PostRepository, get_PostRepository
from .schemas import CreatePost, UpdatePost


class PostService:
    """
    Service class for managing Post entities.
    """

    def __init__(
        self,
        repo: PostRepository,
        category_service: CategoryService,
        tag_service: TagService,
    ):
        """
        Initialize PostService with repository and related services.

        Args:
            repo (PostRepository): The repository instance for Post.
            category_service (CategoryService): Service for category operations.
            tag_service (TagService): Service for tag operations.
        """
        self.repository = repo
        self.category_service = category_service
        self.tag_service = tag_service

    async def create_post(
        self, data: CreatePost, current_user: User, session: AsyncSession
    ) -> Post:
        """
        Create a new post.

        Args:
            data (CreatePost): Data for the new post.
            current_user (User): The current authenticated user.
            session (AsyncSession): Database session.

        Returns:
            Post: The created post instance.

        Raises:
            DuplicateEntryException: If a post with the same title exists.
            InternalException: For unexpected errors.
        """
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
                {
                    **data.model_dump(),
                    "author_id": current_user.id,
                    "categories": categories,
                    "tags": tags,
                },
                session,
            )
        except IntegrityError:
            raise DuplicateEntryException(
                resource=Post.__name__,
                field="title",
                value=data.title,
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
        """
        Update an existing post.

        Args:
            id (int): ID of the post to update.
            update_data (UpdatePost): Data to update.
            session (AsyncSession): Database session.

        Returns:
            Post: The updated post instance.

        Raises:
            DuplicateEntryException: If a post with the same title exists.
            EntityNotFoundException: If the post does not exist.
            InternalException: For unexpected errors.
        """
        post_data = update_data.model_dump(exclude_unset=True)
        try:
            updated_post = await self.repository.get_by_id(id, session)
            if updated_post is None:
                raise EntityNotFoundException(Post.__name__, str(id))

            # Prepare related records if provided
            categories = None
            if update_data.category_ids is not None:
                categories = []
                for category_id in update_data.category_ids:
                    category = await self.category_service.get_category_by_id(
                        category_id, session
                    )
                    categories.append(category)

            tags = None
            if update_data.tag_ids is not None:
                tags = []
                for tag_id in update_data.tag_ids:
                    tag = await self.tag_service.get_tag_by_id(tag_id, session)
                    tags.append(tag)

            # Pass everything to the repository
            result = await self.repository.update_with_m2m(
                updated_post,
                post_data,
                session,
                categories=categories,
                tags=tags,
            )
        except IntegrityError:
            raise DuplicateEntryException(
                resource=Post.__name__,
                field="title",
                value=update_data.title,
            )
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while updating the post.",
                underlying_error=e,
            )

        return result

    async def delete_post(self, id: int, session: AsyncSession) -> Post:
        """
        Delete a post by ID.

        Args:
            id (int): ID of the post to delete.
            session (AsyncSession): Database session.

        Returns:
            Post: The deleted post instance.
        """
        result = await self.repository.delete(id, session)
        return result

    async def get_post_by_id(self, id: int, session: AsyncSession) -> Post:
        """
        Retrieve a post by its ID.

        Args:
            id (int): ID of the post.
            session (AsyncSession): Database session.

        Returns:
            Post: The found post instance.

        Raises:
            EntityNotFoundException: If the post does not exist.
        """
        result = await self.repository.get_by_id(id, session)

        if result is None:
            raise EntityNotFoundException(Post.__name__, str(id))

        return result


@lru_cache
def get_PostService(
    postRepository: Annotated[PostRepository, Depends(get_PostRepository)],
    category_service: Annotated[CategoryService, Depends(get_CategoryService)],
    tag_service: Annotated[TagService, Depends(get_TagService)],
) -> PostService:
    """
    Dependency injector for PostService.

    Args:
        postRepository (PostRepository): The PostRepository instance.
        category_service (CategoryService): The CategoryService instance.
        tag_service (TagService): The TagService instance.

    Returns:
        PostService: The PostService instance.
    """
    return PostService(postRepository, category_service, tag_service)
