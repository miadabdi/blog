from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Column, Enum, Field, Relationship

from ..common.generic_model import GenericModel
from ..common.user_role import UserRole

if TYPE_CHECKING:
    from ..post.models import Post  # Avoid circular import issues


class User(GenericModel, table=True):
    __tablename__: str = "users"  #  type: ignore

    email: EmailStr = Field(index=True, unique=True)
    fname: str = Field(min_length=3)
    lname: str = Field(min_length=3)
    role: UserRole = Field(sa_column=Column(Enum(UserRole)), default=UserRole.USER)
    is_active: bool = Field(default=True)
    is_email_verified: bool = Field(default=False)
    hashed_password: str = Field(default=None)
    password_changed_at: datetime | None = Field(default=None)
    password_reset_token: str | None = Field(default=None)
    password_reset_expires_at: datetime | None = Field(default=None)
    last_login_at: datetime | None = Field(default=None)

    posts: list["Post"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={
            "lazy": "noload",
        },
    )
