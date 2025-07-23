"""
Repository layer for Category.
Handles direct database operations for Category entities.
"""

from functools import lru_cache

from ..common.generic_repository import GenericRepository
from .models import Category


class CategoryRepository(GenericRepository[Category]):
    """
    Repository for Category model, inherits generic CRUD operations.
    """

    def __init__(self):
        super().__init__(Category)


@lru_cache
def get_CategoryRepository():
    """
    Dependency injector for CategoryRepository.
    """
    return CategoryRepository()
