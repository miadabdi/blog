from sqlmodel import Field

from ..common.generic_model import GenericModel


class Comment(GenericModel, table=True):
    __tablename__: str = "comments"  # type: ignore

    post_id: int = Field(foreign_key="posts.id", nullable=False)
    author_name: str = Field(nullable=False)
    author_email: str = Field(nullable=False)
    content: str = Field(nullable=False)
    is_approved: bool = Field(default=True, nullable=False)
    parent_comment_id: int | None = Field(default=None, foreign_key="comments.id")
    user_id: int | None = Field(
        default=None, foreign_key="users.id", ondelete="CASCADE"
    )
