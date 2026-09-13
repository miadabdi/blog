"""
SQLModel definition for Category.
Includes slug generation event listeners.
"""

from typing import TYPE_CHECKING

from slugify import slugify
from sqlalchemy import event
from sqlmodel import Field, Relationship

from ..common.generic_model import GenericModel
from ..post.link_models import PostCategoryLink

if TYPE_CHECKING:
    from ..post.models import Post  # Avoid circular import issues


class Category(GenericModel, table=True):
    """
    SQLModel for the Category entity.
    """

    __tablename__: str = "categories"  # type: ignore

    name: str = Field(unique=True, nullable=False)
    slug: str = Field(unique=True, nullable=False)
    description: str | None = Field(default=None)

    # Relationship to posts via link table
    posts: list["Post"] = Relationship(
        back_populates="categories", link_model=PostCategoryLink
    )


@event.listens_for(Category, "before_insert")
@event.listens_for(Category, "before_update")
def generate_slug(mapper, connection, target: Category):
    """
    SQLAlchemy event listener to generate slug from name before insert/update.

    Args:
        mapper: SQLAlchemy mapper.
        connection: Database connection.
        target (Category): The Category instance being persisted.
    """
    # Only regenerate slug if name exists and (slug is empty or name changed)
    if target.name:
        new_slug = slugify(target.name)
        if not target.slug or target.slug != new_slug:
            target.slug = new_slug
