"""
Pydantic schemas for Post API.
Defines request and response models for post endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from ..auth.schemas import UserPublic
from ..category.schemas import CategoryPublic
from ..tag.schemas import TagPublic


class CreatePost(BaseModel):
    """
    Schema for creating a new post.
    """

    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    body: str = Field(min_length=1)
    featured_image: str = Field(min_length=1)
    category_ids: list[int] | None = Field(default=None)
    tag_ids: list[int] | None = Field(default=None)


class UpdatePost(BaseModel):
    """
    Schema for updating an existing post.
    """

    title: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    body: str | None = Field(default=None)
    featured_image: str | None = Field(default=None)
    category_ids: list[int] | None = Field(default=None)
    tag_ids: list[int] | None = Field(default=None)


class PostPublic(BaseModel):
    """
    Public schema for exposing post data.
    """

    id: int
    title: str
    summary: str
    body: str
    featured_image: str
    slug: str
    published_at: datetime | None
    view_count: int
    categories: list[CategoryPublic] | None
    tags: list[TagPublic] | None
    author_id: int = Field(ge=1)
    author: UserPublic

    class Config:
        from_attributes = True
