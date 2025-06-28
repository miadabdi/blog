from datetime import datetime

from slugify import slugify
from sqlalchemy import event
from sqlmodel import Field

from ..common.generic_model import GenericModel


class Post(GenericModel, table=True):
    __tablename__: str = "posts"  #  type: ignore

    published_at: datetime | None = Field(default=None)
    title: str = Field(min_length=1)
    slug: str = Field(unique=True, min_length=1)
    summary: str = Field(min_length=1)
    body: str = Field(min_length=1)
    featured_image: str = Field(min_length=1)
    view_count: int = Field(default=0)


@event.listens_for(Post, "before_insert")
@event.listens_for(Post, "before_update")
def generate_slug(mapper, connection, target: Post):
    # Only regenerate slug if title exists and (slug is empty or title changed)
    if target.title:
        new_slug = slugify(target.title)
        if not target.slug or target.slug != new_slug:
            target.slug = new_slug
