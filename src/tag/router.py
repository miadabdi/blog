from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ..auth.auth import authorize, get_current_active_user
from ..auth.models import User
from ..common.deps import AsyncSessionDep
from ..common.user_role import UserRole
from .schemas import CreateTag, TagPublic, UpdateTag
from .service import TagService, get_TagService

router = APIRouter(prefix="/tag", tags=["tag"])

TagServiceDep = Annotated[TagService, Depends(get_TagService)]


@router.post("/", response_model=TagPublic)
@authorize(role=[UserRole.ADMIN])
async def create_tag(
    tag: Annotated[CreateTag, Body()],
    session: AsyncSessionDep,
    service: TagServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.create_tag(tag, session)


@router.patch("/{tag_id}", response_model=TagPublic)
@authorize(role=[UserRole.ADMIN])
async def update_tag(
    tag_id: int,
    tag: Annotated[UpdateTag, Body()],
    session: AsyncSessionDep,
    service: TagServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.update_tag(tag_id, tag, session)


@router.delete("/{tag_id}", response_model=TagPublic)
@authorize(role=[UserRole.ADMIN])
async def delete_tag(
    tag_id: int,
    session: AsyncSessionDep,
    service: TagServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.delete_tag(tag_id, session)


@router.get("/{tag_id}", response_model=TagPublic)
async def get_tag_by_id(tag_id: int, session: AsyncSessionDep, service: TagServiceDep):
    return await service.get_tag_by_id(tag_id, session)


@router.get("/", response_model=list[TagPublic])
async def list_tags(session: AsyncSessionDep, service: TagServiceDep):
    return await service.get_all_tags(session)
