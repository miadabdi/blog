from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ..auth.auth import authorize, get_current_active_user
from ..auth.models import User
from ..common.deps import AsyncSessionDep
from ..common.user_role import UserRole
from .schemas import CategoryPublic, CreateCategory, UpdateCategory
from .service import CategoryService, get_CategoryService

router = APIRouter(prefix="/category", tags=["category"])

CategoryServiceDep = Annotated[CategoryService, Depends(get_CategoryService)]


@router.post("/", response_model=CategoryPublic)
@authorize(role=[UserRole.ADMIN])
async def create_category(
    category: Annotated[CreateCategory, Body()],
    session: AsyncSessionDep,
    service: CategoryServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.create_category(category, session)


@router.patch("/{category_id}", response_model=CategoryPublic)
@authorize(role=[UserRole.ADMIN])
async def update_category(
    category_id: int,
    category: Annotated[UpdateCategory, Body()],
    session: AsyncSessionDep,
    service: CategoryServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.update_category(category_id, category, session)


@router.delete("/{category_id}", response_model=CategoryPublic)
@authorize(role=[UserRole.ADMIN])
async def delete_category(
    category_id: int,
    session: AsyncSessionDep,
    service: CategoryServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return await service.delete_category(category_id, session)


@router.get("/{category_id}", response_model=CategoryPublic)
async def get_category_by_id(
    category_id: int, session: AsyncSessionDep, service: CategoryServiceDep
):
    return await service.get_category_by_id(category_id, session)


@router.get("/", response_model=list[CategoryPublic])
async def list_categories(session: AsyncSessionDep, service: CategoryServiceDep):
    return await service.get_all_categories(session)
