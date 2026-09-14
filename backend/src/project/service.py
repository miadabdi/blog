"""
Service layer for Project operations.
Handles business logic and error handling for project CRUD operations.
"""

from datetime import datetime, timezone
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from ..auth.models import User
from ..common.exceptions.exceptions import (
    DuplicateEntryException,
    EntityNotFoundException,
    InternalException,
)
from .models import Project
from .repository import ProjectRepository, get_ProjectRepository
from .schemas import CreateProject, UpdateProject


class ProjectService:
    """
    Service class for managing Project entities.
    """

    def __init__(self, repo: ProjectRepository):
        """
        Initialize ProjectService with repository.

        Args:
            repo (ProjectRepository): The repository instance for Project.
        """
        self.repository = repo

    async def create_project(
        self, data: CreateProject, current_user: User, session: AsyncSession
    ) -> Project:
        """
        Create a new project.

        Args:
            data (CreateProject): Data for the new project.
            current_user (User): The current authenticated user.
            session (AsyncSession): Database session.

        Returns:
            Project: The created project instance.

        Raises:
            DuplicateEntryException: If a project with the same title exists.
            InternalException: For unexpected errors.
        """
        try:
            project_record = await self.repository.create(
                {
                    **data.model_dump(),
                    "author_id": current_user.id,
                    "published_at": datetime.now(timezone.utc).replace(tzinfo=None),
                },
                session,
            )
        except IntegrityError:
            raise DuplicateEntryException(
                resource=Project.__name__,
                field="title",
                value=data.title,
            )
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while creating the project.",
                underlying_error=e,
            )

        return project_record

    async def update_project(
        self, id: int, update_data: UpdateProject, session: AsyncSession
    ) -> Project:
        """
        Update an existing project.

        Args:
            id (int): ID of the project to update.
            update_data (UpdateProject): Data to update.
            session (AsyncSession): Database session.

        Returns:
            Project: The updated project instance.

        Raises:
            DuplicateEntryException: If a project with the same title exists.
            EntityNotFoundException: If the project does not exist.
            InternalException: For unexpected errors.
        """
        try:
            result = await self.repository.update(
                id, update_data.model_dump(exclude_unset=True), session
            )
        except IntegrityError:
            raise DuplicateEntryException(
                resource=Project.__name__,
                field="title",
                value=update_data.title,
            )
        except EntityNotFoundException:
            raise
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while updating the project.",
                underlying_error=e,
            )

        return result

    async def delete_project(self, id: int, session: AsyncSession) -> Project:
        """
        Delete a project by ID.

        Args:
            id (int): ID of the project to delete.
            session (AsyncSession): Database session.

        Returns:
            Project: The deleted project instance.
        """
        return await self.repository.delete(id, session)

    async def get_project_by_id(self, id: int, session: AsyncSession) -> Project:
        """
        Retrieve a project by its ID.

        Args:
            id (int): ID of the project.
            session (AsyncSession): Database session.

        Returns:
            Project: The found project instance.

        Raises:
            EntityNotFoundException: If the project does not exist.
        """
        result = await self.repository.get_by_id(id, session)

        if result is None:
            raise EntityNotFoundException(Project.__name__, str(id))

        return result

    async def get_all_projects(self, session: AsyncSession) -> list[Project]:
        """
        Retrieve all projects, newest first.
        """
        return await self.repository.get_all(session)

    async def get_project_by_slug(self, slug: str, session: AsyncSession) -> Project:
        """
        Retrieve a project by its slug.

        Args:
            slug (str): Slug of the project.
            session (AsyncSession): Database session.

        Returns:
            Project: The found project instance.

        Raises:
            EntityNotFoundException: If the project does not exist.
        """
        result = await self.repository.get_by_slug(slug, session)

        if result is None:
            raise EntityNotFoundException(Project.__name__, slug)

        return result


@lru_cache
def get_ProjectService(
    projectRepository: Annotated[ProjectRepository, Depends(get_ProjectRepository)],
) -> ProjectService:
    """
    Dependency injector for ProjectService.

    Args:
        projectRepository (ProjectRepository): The ProjectRepository instance.

    Returns:
        ProjectService: The ProjectService instance.
    """
    return ProjectService(projectRepository)
