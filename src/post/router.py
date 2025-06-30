from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ..auth.auth import authorize, get_current_active_user
from ..auth.models import User
from ..common.deps import AsyncSessionDep
from ..common.user_role import UserRole
from .schemas import CreatePost, PostPublic, UpdatePost
from .service import PostService, get_PostService

router = APIRouter(prefix="/post", tags=["post"])

PostServiceDep = Annotated[PostService, Depends(get_PostService)]


@router.post("/", response_model=PostPublic)
@authorize(role=[UserRole.ADMIN])
async def create_post(
    post: Annotated[CreatePost, Body()],
    session: AsyncSessionDep,
    service: PostServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.create_post(post, current_user, session)


@router.patch("/{post_id}", response_model=PostPublic)
@authorize(role=[UserRole.ADMIN])
async def update_post(
    post_id: int,
    post: Annotated[UpdatePost, Body()],
    session: AsyncSessionDep,
    service: PostServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.update_post(post_id, post, session)


@router.get("/{post_id}", response_model=PostPublic)
async def get_post_by_id(
    post_id: int, session: AsyncSessionDep, service: PostServiceDep
):
    return await service.get_post_by_id(post_id, session)


@router.delete("/{post_id}", response_model=PostPublic)
@authorize(role=[UserRole.ADMIN])
async def delete_post(
    post_id: int,
    session: AsyncSessionDep,
    service: PostServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.delete_post(post_id, session)
