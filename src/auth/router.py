from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..common.deps import AsyncSessionDep
from .auth import get_current_active_user
from .models import User
from .schemas import SignUp, Token, UserPublic
from .service import UserService, get_UserService

router = APIRouter(prefix="/auth", tags=["auth"])

UserServiceDep = Annotated[UserService, Depends(get_UserService)]


@router.post(
    "/signup",
    response_model=UserPublic,
)
async def signup(
    form_data: Annotated[SignUp, Body()],
    user_service: Annotated[UserService, Depends(get_UserService)],
    session: AsyncSessionDep,
):
    return await user_service.sign_up(form_data, session)


@router.post(
    "/signin",
    response_model=Token,
)
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSessionDep,
    user_service: Annotated[UserService, Depends(get_UserService)],
) -> Token:
    return await user_service.sign_in(form_data, session)


@router.get(
    "/get-me",
    response_model=UserPublic,
)
async def getMe(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
