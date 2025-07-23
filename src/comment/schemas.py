"""
Pydantic schemas for Comment API.
Defines request and response models for comment endpoints.
"""

from pydantic import BaseModel, EmailStr, Field


class CreateComment(BaseModel):
    """
    Schema for creating a new comment.
    """

    post_id: int
    author_name: str | None = Field(default=None, min_length=1)
    author_email: EmailStr | None = None
    content: str = Field(min_length=1)
    parent_comment_id: int | None = None


class CommentPublic(BaseModel):
    """
    Public schema for exposing comment data.
    """

    id: int
    post_id: int
    author_name: str
    author_email: EmailStr
    content: str
    is_approved: bool
    parent_comment_id: int | None
    user_id: int | None

    class Config:
        from_attributes = True
