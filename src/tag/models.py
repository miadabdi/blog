"""
SQLModel definition for Tag.
Includes slug generation event listeners and relationships.
"""

from typing import TYPE_CHECKING

from slugify import slugify
from sqlalchemy import event
from sqlmodel import Field, Relationship

from ..common.generic_model import GenericModel
from ..post.link_models import PostTagLink

if TYPE_CHECKING:
    from ..post.models import Post


class Tag(GenericModel, table=True):
    """
    SQLModel for the Tag entity.
    """

    __tablename__: str = "tags"  # type: ignore

    name: str = Field(unique=True, nullable=False)
    slug: str = Field(unique=True, nullable=False)

    posts: list["Post"] = Relationship(
        back_populates="tags",
        link_model=PostTagLink,
    )


@event.listens_for(Tag, "before_insert")
@event.listens_for(Tag, "before_update")
def generate_slug(mapper, connection, target: Tag):
    """
    SQLAlchemy event listener to generate slug from name before insert/update.

    Args:
        mapper: SQLAlchemy mapper.
        connection: Database connection.
        target (Tag): The Tag instance being persisted.
    """
    # Only regenerate slug if name exists and (slug is empty or name changed)
    if target.name:
        new_slug = slugify(target.name)
        if not target.slug or target.slug != new_slug:
            target.slug = new_slug
