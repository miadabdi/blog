from functools import lru_cache
from .models import Post
from ..common.generic_repository import GenericRepository

class PostRepository(GenericRepository[Post]):
    def __init__(self):
        print("POST REPO CREATED")
        super().__init__(Post)

@lru_cache
def get_PostRepository():
    return PostRepository()
