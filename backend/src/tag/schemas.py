"""
Pydantic schemas for Tag API.
Defines request and response models for tag endpoints.
"""

from pydantic import BaseModel, Field


class CreateTag(BaseModel):
    """
    Schema for creating a new tag.
    """

    name: str = Field(min_length=1)


class UpdateTag(BaseModel):
    """
    Schema for updating an existing tag.
    """

    name: str | None = None


class TagPublic(BaseModel):
    """
    Public schema for exposing tag data.
    """

    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True
