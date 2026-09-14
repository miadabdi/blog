"""
Pydantic schemas for Project API.
Defines request and response models for project endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from ..auth.schemas import UserPublic


class CreateProject(BaseModel):
    """
    Schema for creating a new project.
    """

    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    body: dict
    tech: list[str] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)
    github_url: str | None = Field(default=None)
    demo_url: str | None = Field(default=None)
    featured: bool = Field(default=False)


class UpdateProject(BaseModel):
    """
    Schema for updating an existing project.
    """

    title: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    body: dict | None = Field(default=None)
    tech: list[str] | None = Field(default=None)
    images: list[str] | None = Field(default=None)
    github_url: str | None = Field(default=None)
    demo_url: str | None = Field(default=None)
    featured: bool | None = Field(default=None)


class ProjectPublic(BaseModel):
    """
    Public schema for exposing project data.
    """

    id: int
    title: str
    slug: str
    summary: str
    body: dict
    featured: bool
    view_count: int
    published_at: datetime | None
    created_at: datetime
    tech: list[str]
    images: list[str]
    github_url: str | None
    demo_url: str | None
    author_id: int = Field(ge=1)
    author: UserPublic

    class Config:
        from_attributes = True
