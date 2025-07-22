from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from ..common.deps import AsyncSessionDep
from ..common.http_responses.doc_responses import (
    ResponseErrorDoc,
    ResponseSuccessDoc,
)
from ..common.http_responses.success_response import SuccessCodes, SuccessResponse
from ..common.http_responses.success_result import SuccessResult
from .auth import get_current_active_user
from .models import User
from .schemas import SignUp, Token, UserPublic
from .service import UserService, get_UserService

router = APIRouter(prefix="/auth", tags=["auth"])

UserServiceDep = Annotated[UserService, Depends(get_UserService)]


@router.post(
    "/signup",
    response_model=UserPublic,
    responses={
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_409_CONFLICT(),
    },
)
async def signup(
    form_data: Annotated[SignUp, Body()],
    user_service: Annotated[UserService, Depends(get_UserService)],
    session: AsyncSessionDep,
    request: Request,
):
    user = await user_service.sign_up(form_data, session)

    # Convert User to UserPublic, removes sensitive fields
    user_public = UserPublic.model_validate(user)
    result = SuccessResult[UserPublic](
        code=SuccessCodes.SUCCESS,
        message="User fetched successfully",
        status_code=status.HTTP_200_OK,
        data=user_public,
    )

    return result.to_json_response(request)


@router.post(
    "/token",
    status_code=201,
    response_model=Token,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Token created successfully", Token),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED(),
    },
)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSessionDep,
    user_service: Annotated[UserService, Depends(get_UserService)],
):
    result = await user_service.sign_in(form_data, session)
    return result


@router.post(
    "/signin",
    status_code=201,
    response_model=SuccessResponse[Token],
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Token created successfully", Token),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED(),
    },
)
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSessionDep,
    user_service: Annotated[UserService, Depends(get_UserService)],
    request: Request,
):
    result = await token(form_data, session, user_service)

    result = SuccessResult[Token](
        code=SuccessCodes.CREATED,
        message="Tokens created successfully",
        status_code=status.HTTP_201_CREATED,
        data=result,
    )

    return result.to_json_response(request)


@router.get(
    "/get-me",
    response_model=SuccessResult[UserPublic],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR(),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND(),
        **ResponseErrorDoc.HTTP_401_UNAUTHORIZED(),
    },
)
async def getMe(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
):
    # Convert User to UserPublic, removes sensitive fields
    user_public = UserPublic.model_validate(current_user)
    result = SuccessResult[UserPublic](
        code=SuccessCodes.SUCCESS,
        message="User fetched successfully",
        status_code=status.HTTP_200_OK,
        data=user_public,
    )

    return result.to_json_response(request)
