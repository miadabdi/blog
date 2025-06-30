from slugify import slugify
from sqlalchemy import event
from sqlmodel import Field

from ..common.generic_model import GenericModel


class Category(GenericModel, table=True):
    __tablename__: str = "categories"  # type: ignore

    name: str = Field(unique=True, nullable=False)
    slug: str = Field(unique=True, nullable=False)
    description: str | None = Field(default=None)


@event.listens_for(Category, "before_insert")
@event.listens_for(Category, "before_update")
def generate_slug(mapper, connection, target: Category):
    # Only regenerate slug if name exists and (slug is empty or name changed)
    if target.name:
        new_slug = slugify(target.name)
        if not target.slug or target.slug != new_slug:
            target.slug = new_slug
