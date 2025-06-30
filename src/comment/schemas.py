from pydantic import BaseModel, EmailStr, Field


class CreateComment(BaseModel):
    post_id: int
    author_name: str | None = Field(default=None, min_length=1)
    author_email: EmailStr | None = None
    content: str = Field(min_length=1)
    parent_comment_id: int | None = None


class CommentPublic(BaseModel):
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
