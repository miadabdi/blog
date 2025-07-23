"""
Service layer for Category operations.
Handles business logic and error handling for category CRUD operations.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from ..common.exceptions.exceptions import (
    DuplicateEntryException,
    EntityNotFoundException,
    InternalException,
)
from .models import Category
from .repository import CategoryRepository, get_CategoryRepository
from .schemas import CreateCategory, UpdateCategory


class CategoryService:
    """
    Service class for managing Category entities.
    """

    def __init__(self, repo: CategoryRepository):
        """
        Initialize the CategoryService with a repository.
        """
        self.repository = repo

    async def create_category(
        self, data: CreateCategory, session: AsyncSession
    ) -> Category:
        """
        Create a new category.

        Args:
            data (CreateCategory): Data for the new category.
            session (AsyncSession): Database session.

        Returns:
            Category: The created category instance.

        Raises:
            DuplicateEntryException: If a category with the same name exists.
            InternalException: For unexpected errors.
        """
        try:
            # Attempt to create the category in the repository
            category_record = await self.repository.create(data.model_dump(), session)
        except IntegrityError:
            # Handle duplicate name error
            raise DuplicateEntryException(
                field="name",
                value=f"{data.name}",
                resource=Category.__name__,
            )
        except Exception as e:
            # Handle any other unexpected errors
            raise InternalException(
                message="An unexpected error occurred while creating the category.",
                underlying_error=e,
            )
        return category_record

    async def update_category(
        self, id: int, update_data: UpdateCategory, session: AsyncSession
    ) -> Category:
        """
        Update an existing category.

        Args:
            id (int): ID of the category to update.
            update_data (UpdateCategory): Data to update.
            session (AsyncSession): Database session.

        Returns:
            Category: The updated category instance.

        Raises:
            DuplicateEntryException: If a category with the same name exists.
            InternalException: For unexpected errors.
        """
        category_data = update_data.model_dump(exclude_unset=True)
        try:
            updated_category = await self.repository.update(id, category_data, session)
        except IntegrityError:
            raise DuplicateEntryException(
                field="name",
                value=f"{update_data.name}",
                resource=Category.__name__,
            )
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while updating the category.",
                underlying_error=e,
            )
        return updated_category

    async def delete_category(self, id: int, session: AsyncSession) -> Category:
        """
        Delete a category by ID.

        Args:
            id (int): ID of the category to delete.
            session (AsyncSession): Database session.

        Returns:
            Category: The deleted category instance.
        """
        result = await self.repository.delete(id, session)
        return result

    async def get_category_by_id(self, id: int, session: AsyncSession) -> Category:
        """
        Retrieve a category by its ID.

        Args:
            id (int): ID of the category.
            session (AsyncSession): Database session.

        Returns:
            Category: The found category instance.

        Raises:
            EntityNotFoundException: If the category does not exist.
        """
        result = await self.repository.get_by_id(id, session)
        if result is None:
            raise EntityNotFoundException(str(id), Category.__name__)
        return result

    async def get_all_categories(self, session: AsyncSession) -> list[Category]:
        """
        Retrieve all categories.

        Args:
            session (AsyncSession): Database session.

        Returns:
            list[Category]: List of all categories.
        """
        return await self.repository.get_all(session)


@lru_cache
def get_CategoryService(
    categoryRepository: Annotated[CategoryRepository, Depends(get_CategoryRepository)],
) -> CategoryService:
    """
    Dependency injector for CategoryService.
    """
    return CategoryService(categoryRepository)
