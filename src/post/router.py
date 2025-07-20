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
from .schemas import CreatePost, PostPublic, UpdatePost
from .service import PostService, get_PostService

router = APIRouter(prefix="/post", tags=["post"])

PostServiceDep = Annotated[PostService, Depends(get_PostService)]


@router.post(
    "/",
    response_model=SuccessResult[PostPublic],
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Post created successfully", PostPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def create_post(
    post: Annotated[CreatePost, Body()],
    session: AsyncSessionDep,
    service: PostServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    created_post = await service.create_post(post, current_user, session)
    public_post = PostPublic.model_validate(created_post)
    result = SuccessResult[PostPublic](
        code=SuccessCodes.CREATED,
        message="Post created successfully",
        status_code=status.HTTP_201_CREATED,
        data=public_post,
    )
    return result.to_json_response(request)


@router.patch(
    "/{post_id}",
    response_model=SuccessResult[PostPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Post updated successfully", PostPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def update_post(
    post_id: int,
    post: Annotated[UpdatePost, Body()],
    session: AsyncSessionDep,
    service: PostServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    updated_post = await service.update_post(post_id, post, session)
    public_post = PostPublic.model_validate(updated_post)
    result = SuccessResult[PostPublic](
        code=SuccessCodes.SUCCESS,
        message="Post updated successfully",
        status_code=status.HTTP_200_OK,
        data=public_post,
    )
    return result.to_json_response(request)


@router.get(
    "/{post_id}",
    response_model=SuccessResult[PostPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Post fetched successfully", PostPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
    },
)
async def get_post_by_id(
    post_id: int, session: AsyncSessionDep, service: PostServiceDep, request: Request
):
    post = await service.get_post_by_id(post_id, session)
    public_post = PostPublic.model_validate(post)
    result = SuccessResult[PostPublic](
        code=SuccessCodes.SUCCESS,
        message="Post fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_post,
    )
    return result.to_json_response(request)


@router.delete(
    "/{post_id}",
    response_model=SuccessResult[PostPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Post deleted successfully", PostPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def delete_post(
    post_id: int,
    session: AsyncSessionDep,
    service: PostServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    deleted_post = await service.delete_post(post_id, session)
    public_post = PostPublic.model_validate(deleted_post)
    result = SuccessResult[PostPublic](
        code=SuccessCodes.SUCCESS,
        message="Post deleted successfully",
        status_code=status.HTTP_200_OK,
        data=public_post,
    )
    return result.to_json_response(request)
