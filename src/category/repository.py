from functools import lru_cache

from ..common.generic_repository import GenericRepository
from .models import Category


class CategoryRepository(GenericRepository[Category]):
    def __init__(self):
        super().__init__(Category)


@lru_cache
def get_CategoryRepository():
    return CategoryRepository()
