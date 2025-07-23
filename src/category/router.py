"""
API router for Category endpoints.
Handles HTTP requests for category CRUD operations.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request, status

from ..auth.auth import authorize, get_current_active_user
from ..auth.models import User
from ..common.deps import AsyncSessionDep
from ..common.http_responses.doc_responses import (
    ResponseErrorDoc,
    ResponseSuccessDoc,
)
from ..common.http_responses.success_response import SuccessCodes
from ..common.http_responses.success_result import SuccessResult
from ..common.user_role import UserRole
from .schemas import CategoryPublic, CreateCategory, UpdateCategory
from .service import CategoryService, get_CategoryService

router = APIRouter(prefix="/category", tags=["category"])

CategoryServiceDep = Annotated[CategoryService, Depends(get_CategoryService)]


@router.post(
    "/",
    response_model=SuccessResult[CategoryPublic],
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED(
            "Category created successfully", CategoryPublic
        ),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def create_category(
    category: Annotated[CreateCategory, Body()],
    session: AsyncSessionDep,
    service: CategoryServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """
    Create a new category.

    Args:
        category (CreateCategory): The category data to create.
        session (AsyncSessionDep): The database session.
        service (CategoryServiceDep): The category service dependency.
        current_user (User): The current authenticated user.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: The created category wrapped in a SuccessResult.
    """
    created_category = await service.create_category(category, session)

    public_category = CategoryPublic.model_validate(created_category)

    result = SuccessResult[CategoryPublic](
        code=SuccessCodes.CREATED,
        message="Category created successfully",
        status_code=status.HTTP_201_CREATED,
        data=public_category,
    )

    return result.to_json_response(request)


@router.patch(
    "/{category_id}",
    response_model=CategoryPublic,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK(
            "Category updated successfully", CategoryPublic
        ),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def update_category(
    category_id: int,
    category: Annotated[UpdateCategory, Body()],
    session: AsyncSessionDep,
    service: CategoryServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """
    Update an existing category.

    Args:
        category_id (int): The ID of the category to update.
        category (UpdateCategory): The updated category data.
        session (AsyncSessionDep): The database session.
        service (CategoryServiceDep): The category service dependency.
        current_user (User): The current authenticated user.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: The updated category wrapped in a SuccessResult.
    """
    updated_category = await service.update_category(category_id, category, session)

    public_category = CategoryPublic.model_validate(updated_category)

    result = SuccessResult[CategoryPublic](
        code=SuccessCodes.SUCCESS,
        message="Category Updated successfully",
        status_code=status.HTTP_200_OK,
        data=public_category,
    )

    return result.to_json_response(request)


@router.delete(
    "/{category_id}",
    response_model=SuccessResult[CategoryPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK(
            "Category deleted successfully", CategoryPublic
        ),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def delete_category(
    category_id: int,
    session: AsyncSessionDep,
    service: CategoryServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """
    Delete a category by its ID.

    Args:
        category_id (int): The ID of the category to delete.
        session (AsyncSessionDep): The database session.
        service (CategoryServiceDep): The category service dependency.
        current_user (User): The current authenticated user.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: The deleted category wrapped in a SuccessResult.
    """
    deleted_category = await service.delete_category(category_id, session)

    public_category = CategoryPublic.model_validate(deleted_category)
    result = SuccessResult[CategoryPublic](
        code=SuccessCodes.SUCCESS,
        message="Category Deleted successfully",
        status_code=status.HTTP_200_OK,
        data=public_category,
    )

    return result.to_json_response(request)


@router.get(
    "/{category_id}",
    response_model=SuccessResult[CategoryPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK(
            "Category fetched successfully", CategoryPublic
        ),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
    },
)
async def get_category_by_id(
    category_id: int,
    session: AsyncSessionDep,
    service: CategoryServiceDep,
    request: Request,
):
    """
    Retrieve a category by its ID.

    Args:
        category_id (int): The ID of the category to retrieve.
        session (AsyncSessionDep): The database session.
        service (CategoryServiceDep): The category service dependency.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: The requested category wrapped in a SuccessResult.
    """
    category = await service.get_category_by_id(category_id, session)

    public_category = CategoryPublic.model_validate(category)

    result = SuccessResult[CategoryPublic](
        code=SuccessCodes.SUCCESS,
        message="Category fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_category,
    )

    return result.to_json_response(request)


@router.get(
    "/",
    response_model=SuccessResult[list[CategoryPublic]],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK(
            "Categories fetched successfully", CategoryPublic
        ),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
    },
)
async def list_categories(
    session: AsyncSessionDep, service: CategoryServiceDep, request: Request
):
    """
    Retrieve all categories.

    Args:
        session (AsyncSessionDep): The database session.
        service (CategoryServiceDep): The category service dependency.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: A list of categories wrapped in a SuccessResult.
    """
    categories = await service.get_all_categories(session)

    public_categories = [
        CategoryPublic.model_validate(category) for category in categories
    ]

    result = SuccessResult[list[CategoryPublic]](
        code=SuccessCodes.SUCCESS,
        message="Category fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_categories,
    )

    return result.to_json_response(request)
