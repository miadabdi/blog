from datetime import datetime

from pydantic import BaseModel, Field

from ..category.schemas import CategoryPublic
from ..tag.schemas import TagPublic  # <-- Add this import


class CreatePost(BaseModel):
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    body: str = Field(min_length=1)
    featured_image: str = Field(min_length=1)
    category_ids: list[int] | None = Field(default=None)
    tag_ids: list[int] | None = Field(default=None)  # <-- Add this field


class UpdatePost(BaseModel):
    title: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    body: str | None = Field(default=None)
    featured_image: str | None = Field(default=None)
    category_ids: list[int] | None = Field(default=None)
    tag_ids: list[int] | None = Field(default=None)  # <-- Add this field


class PostPublic(BaseModel):
    id: int
    title: str
    summary: str
    body: str
    featured_image: str
    slug: str
    published_at: datetime | None
    view_count: int
    categories: list[CategoryPublic] | None
    tags: list[TagPublic] | None  # <-- Add this field

    class Config:
        from_attributes = True
