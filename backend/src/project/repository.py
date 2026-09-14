"""
Repository layer for Project.
Handles direct database operations for Project entities.
"""

from functools import lru_cache

from sqlmodel import select

from ..common.generic_repository import GenericRepository
from .models import Project


class ProjectRepository(GenericRepository[Project]):
    """
    Repository for Project model, inherits generic CRUD operations.
    """

    def __init__(self):
        super().__init__(Project)

    async def get_all(self, session) -> list[Project]:
        """
        Get all projects, newest first.
        """
        return list(
            (
                await session.exec(
                    select(self.model).order_by(self.model.created_at.desc())
                )
            ).all()
        )

    async def get_by_slug(self, slug: str, session) -> Project | None:
        """
        Get a project by its slug.
        """
        return (
            await session.exec(select(self.model).where(self.model.slug == slug))
        ).first()


@lru_cache
def get_ProjectRepository():
    """
    Dependency injector for ProjectRepository.
    """
    return ProjectRepository()
