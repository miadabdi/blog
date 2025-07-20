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
from .schemas import CreateTag, TagPublic, UpdateTag
from .service import TagService, get_TagService

router = APIRouter(prefix="/tag", tags=["tag"])

TagServiceDep = Annotated[TagService, Depends(get_TagService)]


@router.post(
    "/",
    response_model=SuccessResult[TagPublic],
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Tag created successfully", TagPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def create_tag(
    tag: Annotated[CreateTag, Body()],
    session: AsyncSessionDep,
    service: TagServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    created_tag = await service.create_tag(tag, session)
    public_tag = TagPublic.model_validate(created_tag)
    result = SuccessResult[TagPublic](
        code=SuccessCodes.CREATED,
        message="Tag created successfully",
        status_code=status.HTTP_201_CREATED,
        data=public_tag,
    )
    return result.to_json_response(request)


@router.patch(
    "/{tag_id}",
    response_model=SuccessResult[TagPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Tag updated successfully", TagPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def update_tag(
    tag_id: int,
    tag: Annotated[UpdateTag, Body()],
    session: AsyncSessionDep,
    service: TagServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    updated_tag = await service.update_tag(tag_id, tag, session)
    public_tag = TagPublic.model_validate(updated_tag)
    result = SuccessResult[TagPublic](
        code=SuccessCodes.SUCCESS,
        message="Tag updated successfully",
        status_code=status.HTTP_200_OK,
        data=public_tag,
    )
    return result.to_json_response(request)


@router.delete(
    "/{tag_id}",
    response_model=SuccessResult[TagPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Tag deleted successfully", TagPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def delete_tag(
    tag_id: int,
    session: AsyncSessionDep,
    service: TagServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    deleted_tag = await service.delete_tag(tag_id, session)
    public_tag = TagPublic.model_validate(deleted_tag)
    result = SuccessResult[TagPublic](
        code=SuccessCodes.SUCCESS,
        message="Tag deleted successfully",
        status_code=status.HTTP_200_OK,
        data=public_tag,
    )
    return result.to_json_response(request)


@router.get(
    "/{tag_id}",
    response_model=SuccessResult[TagPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Tag fetched successfully", TagPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
    },
)
async def get_tag_by_id(
    tag_id: int, session: AsyncSessionDep, service: TagServiceDep, request: Request
):
    tag = await service.get_tag_by_id(tag_id, session)
    public_tag = TagPublic.model_validate(tag)
    result = SuccessResult[TagPublic](
        code=SuccessCodes.SUCCESS,
        message="Tag fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_tag,
    )
    return result.to_json_response(request)


@router.get(
    "/",
    response_model=SuccessResult[list[TagPublic]],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Tags fetched successfully", TagPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
    },
)
async def list_tags(session: AsyncSessionDep, service: TagServiceDep, request: Request):
    tags = await service.get_all_tags(session)
    public_tags = [TagPublic.model_validate(tag) for tag in tags]
    result = SuccessResult[list[TagPublic]](
        code=SuccessCodes.SUCCESS,
        message="Tags fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_tags,
    )
    return result.to_json_response(request)
