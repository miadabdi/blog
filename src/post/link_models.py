"""
Link models for many-to-many relationships between Post, Category, and Tag.
"""

from sqlmodel import Field, SQLModel


class PostCategoryLink(SQLModel, table=True):
    """
    Link table for Post and Category many-to-many relationship.
    """

    post_id: int = Field(foreign_key="posts.id", primary_key=True)
    category_id: int = Field(foreign_key="categories.id", primary_key=True)


class PostTagLink(SQLModel, table=True):
    """
    Link table for Post and Tag many-to-many relationship.
    """

    post_id: int = Field(foreign_key="posts.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
