from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from ..auth.models import User
from ..common.exceptions.exceptions import EntityNotFoundException, InternalException
from .models import Comment
from .repository import CommentRepository, get_CommentRepository
from .schemas import CreateComment


class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repository = repo

    async def create_comment(
        self,
        data: CreateComment,
        session: AsyncSession,
        user_id: int | None = None,
        current_user: User | None = None,
    ) -> Comment:
        comment_data = data.model_dump()
        if user_id and current_user:
            comment_data["user_id"] = user_id
            comment_data["author_name"] = f"{current_user.fname} {current_user.lname}"
            comment_data["author_email"] = current_user.email
        else:
            if not comment_data.get("author_name") or not comment_data.get(
                "author_email"
            ):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="author_name and author_email are required for anonymous comments.",
                )
        try:
            comment_record = await self.repository.create(comment_data, session)
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while creating the comment.",
                underlying_error=e,
            )
        return comment_record

    async def get_comments_by_post(
        self, post_id: int, session: AsyncSession
    ) -> list[Comment]:
        return await self.repository.get_by_post_id(post_id, session)

    async def delete_comment(
        self,
        comment_id: int,
        session: AsyncSession,
    ) -> Comment:
        comment = await self.repository.get_by_id(comment_id, session)
        if not comment:
            raise EntityNotFoundException(
                str(comment_id),
                Comment.__name__,
            )

        await session.delete(comment)
        return comment


@lru_cache
def get_CommentService(
    commentRepository: Annotated[CommentRepository, Depends(get_CommentRepository)],
) -> CommentService:
    return CommentService(commentRepository)
