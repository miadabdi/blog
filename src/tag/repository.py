from functools import lru_cache

from ..common.generic_repository import GenericRepository
from .models import Tag


class TagRepository(GenericRepository[Tag]):
    def __init__(self):
        super().__init__(Tag)


@lru_cache
def get_TagRepository():
    return TagRepository()
