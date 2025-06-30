from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ..auth.auth import authorize, get_current_active_user
from ..auth.models import User
from ..common.deps import AsyncSessionDep
from ..common.user_role import UserRole
from .schemas import CommentPublic, CreateComment
from .service import CommentService, get_CommentService

router = APIRouter(prefix="/comment", tags=["comment"])

CommentServiceDep = Annotated[CommentService, Depends(get_CommentService)]


@router.post("/", response_model=CommentPublic)
async def create_comment(
    comment: Annotated[CreateComment, Body()],
    session: AsyncSessionDep,
    service: CommentServiceDep,
    current_user: Annotated[User | None, Depends(get_current_active_user)] = None,
):
    user_id = current_user.id if current_user else None
    result = await service.create_comment(comment, session, user_id, current_user)
    await session.commit()
    return result


@router.get("/by-post/{post_id}", response_model=list[CommentPublic])
async def list_comments(
    post_id: int, session: AsyncSessionDep, service: CommentServiceDep
):
    result = await service.get_comments_by_post(post_id, session)
    await session.commit()
    return result


@router.delete("/{comment_id}", response_model=CommentPublic)
@authorize(role=[UserRole.ADMIN])
async def delete_comment(
    comment_id: int,
    session: AsyncSessionDep,
    service: CommentServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    result = await service.delete_comment(comment_id, session)
    await session.commit()
    return result
