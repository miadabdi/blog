"""
SQLModel definition for Project.
Includes slug generation event listener and author relationship.
"""

from datetime import datetime

from slugify import slugify
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship

from ..auth.models import User
from ..common.generic_model import GenericModel


class Project(GenericModel, table=True):
    """
    SQLModel for the Project entity.
    """

    __tablename__: str = "projects"  #  type: ignore

    published_at: datetime | None = Field(default=None)
    title: str = Field(min_length=1)
    slug: str = Field(unique=True, min_length=1)
    summary: str = Field(min_length=1)
    featured: bool = Field(default=False)
    view_count: int = Field(default=0)

    body: dict = Field(sa_type=JSONB, nullable=False)
    tech: list[str] = Field(sa_type=JSONB, nullable=False)
    images: list[str] = Field(sa_type=JSONB, nullable=False)

    github_url: str | None = Field(default=None)
    demo_url: str | None = Field(default=None)

    author_id: int = Field(foreign_key="users.id", nullable=False)
    author: User = Relationship(
        back_populates="projects",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    class Config:  # type: ignore
        arbitrary_types_allowed = True


@event.listens_for(Project, "before_insert")
@event.listens_for(Project, "before_update")
def generate_slug(mapper, connection, target: Project):
    """
    SQLAlchemy event listener to generate slug from title before insert/update.
    """
    if target.title:
        new_slug = slugify(target.title)
        if not target.slug or target.slug != new_slug:
            target.slug = new_slug
