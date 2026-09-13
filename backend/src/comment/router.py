"""
API router for Comment endpoints.
Handles HTTP requests for comment CRUD operations.
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
from .schemas import CommentPublic, CreateComment
from .service import CommentService, get_CommentService

router = APIRouter(prefix="/comment", tags=["comment"])

CommentServiceDep = Annotated[CommentService, Depends(get_CommentService)]


@router.post(
    "/",
    response_model=SuccessResult[CommentPublic],
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED(
            "Comment created successfully", CommentPublic
        ),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
    },
)
async def create_comment(
    comment: Annotated[CreateComment, Body()],
    session: AsyncSessionDep,
    service: CommentServiceDep,
    request: Request,
    current_user: Annotated[User | None, Depends(get_current_active_user)] = None,
):
    """
    Create a new comment.

    Args:
        comment (CreateComment): The comment data to create.
        session (AsyncSessionDep): The database session.
        service (CommentServiceDep): The comment service dependency.
        request (Request): The HTTP request object.
        current_user (User | None): The current authenticated user, if any.

    Returns:
        JSONResponse: The created comment wrapped in a SuccessResult.
    """
    user_id = current_user.id if current_user else None
    created_comment = await service.create_comment(
        comment, session, user_id, current_user
    )
    public_comment = CommentPublic.model_validate(created_comment)
    result = SuccessResult[CommentPublic](
        code=SuccessCodes.CREATED,
        message="Comment created successfully",
        status_code=status.HTTP_201_CREATED,
        data=public_comment,
    )
    return result.to_json_response(request)


@router.get(
    "/by-post/{post_id}",
    response_model=SuccessResult[list[CommentPublic]],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK(
            "Comments fetched successfully", CommentPublic
        ),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
    },
)
async def list_comments(
    post_id: int, session: AsyncSessionDep, service: CommentServiceDep, request: Request
):
    """
    Retrieve all comments for a given post.

    Args:
        post_id (int): The ID of the post to fetch comments for.
        session (AsyncSessionDep): The database session.
        service (CommentServiceDep): The comment service dependency.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: A list of comments wrapped in a SuccessResult.
    """
    comments = await service.get_comments_by_post(post_id, session)
    public_comments = [CommentPublic.model_validate(comment) for comment in comments]
    result = SuccessResult[list[CommentPublic]](
        code=SuccessCodes.SUCCESS,
        message="Comments fetched successfully",
        status_code=status.HTTP_200_OK,
        data=public_comments,
    )
    return result.to_json_response(request)


@router.delete(
    "/{comment_id}",
    response_model=SuccessResult[CommentPublic],
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Comment deleted successfully", CommentPublic),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_403_FORBIDDEN(),
    },
)
@authorize(role=[UserRole.ADMIN])
async def delete_comment(
    comment_id: int,
    session: AsyncSessionDep,
    service: CommentServiceDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    """
    Delete a comment by its ID.

    Args:
        comment_id (int): The ID of the comment to delete.
        session (AsyncSessionDep): The database session.
        service (CommentServiceDep): The comment service dependency.
        current_user (User): The current authenticated user.
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: The deleted comment wrapped in a SuccessResult.
    """
    deleted_comment = await service.delete_comment(comment_id, session)
    public_comment = CommentPublic.model_validate(deleted_comment)
    result = SuccessResult[CommentPublic](
        code=SuccessCodes.SUCCESS,
        message="Comment deleted successfully",
        status_code=status.HTTP_200_OK,
        data=public_comment,
    )
    return result.to_json_response(request)
