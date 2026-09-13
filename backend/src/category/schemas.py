"""
Pydantic schemas for Category API.
Defines request and response models for category endpoints.
"""

from pydantic import BaseModel, Field


class CreateCategory(BaseModel):
    """
    Schema for creating a new category.
    """

    name: str = Field(min_length=1)
    description: str | None = None


class UpdateCategory(BaseModel):
    """
    Schema for updating an existing category.
    """

    name: str | None = None
    description: str | None = None


class CategoryPublic(BaseModel):
    """
    Public schema for exposing category data.
    """

    id: int
    name: str
    slug: str
    description: str | None

    class Config:
        from_attributes = True
