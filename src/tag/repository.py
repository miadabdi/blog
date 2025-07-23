"""
Repository layer for Tag.
Handles direct database operations for Tag entities.
"""

from functools import lru_cache

from ..common.generic_repository import GenericRepository
from .models import Tag


class TagRepository(GenericRepository[Tag]):
    """
    Repository for Tag model, inherits generic CRUD operations.
    """

    def __init__(self):
        super().__init__(Tag)


@lru_cache
def get_TagRepository():
    """
    Dependency injector for TagRepository.
    """
    return TagRepository()
