"""
SQLModel definition for Post.
Includes slug generation event listeners and relationships.
"""

from datetime import datetime

from slugify import slugify
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship

from ..auth.models import User
from ..category.models import Category
from ..common.generic_model import GenericModel
from ..tag.models import Tag
from .link_models import (
    PostCategoryLink,
    PostTagLink,
)


class Post(GenericModel, table=True):
    """
    SQLModel for the Post entity.
    """

    __tablename__: str = "posts"  #  type: ignore

    published_at: datetime | None = Field(default=None)
    title: str = Field(min_length=1)
    slug: str = Field(unique=True, min_length=1)
    summary: str = Field(min_length=1)
    featured_image: str = Field(min_length=1)
    view_count: int = Field(default=0)

    body: dict = Field(sa_type=JSONB, nullable=False)

    author_id: int = Field(foreign_key="users.id", nullable=False)
    author: User = Relationship(
        back_populates="posts",
        sa_relationship_kwargs={"lazy": "select"},
    )

    categories: list[Category] = Relationship(
        back_populates="posts",
        link_model=PostCategoryLink,
        sa_relationship_kwargs={"lazy": "select"},
    )
    tags: list[Tag] = Relationship(
        back_populates="posts",
        link_model=PostTagLink,
        sa_relationship_kwargs={"lazy": "select"},
    )

    class Config:  # type: ignore
        arbitrary_types_allowed = True


@event.listens_for(Post, "before_insert")
@event.listens_for(Post, "before_update")
def generate_slug(mapper, connection, target: Post):
    """
    SQLAlchemy event listener to generate slug from title before insert/update.

    Args:
        mapper: SQLAlchemy mapper.
        connection: Database connection.
        target (Post): The Post instance being persisted.
    """
    # Only regenerate slug if title exists and (slug is empty or title changed)
    if target.title:
        new_slug = slugify(target.title)
        if not target.slug or target.slug != new_slug:
            target.slug = new_slug
