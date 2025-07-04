from datetime import datetime, timedelta, timezone
from functools import lru_cache, wraps
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from ..common.deps import AsyncSessionDep
from ..common.exceptions.forbidden import ForbiddenException
from ..common.exceptions.internal import InternalException
from ..common.exceptions.unauthorized import UnauthorizedException
from ..common.handle_sync import _handle_sync
from ..common.settings import settings
from .models import User
from .repository import UserRepository, get_UserRepository
from .schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @_handle_sync
    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    @_handle_sync
    def get_password_hash(self, password: str):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    async def verify_user(self, token: str, session: AsyncSession):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username = payload.get("sub")
            if username is None:
                raise UnauthorizedException()
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise UnauthorizedException()
        except Exception:
            raise InternalException()

        user = await self.user_repository.get_by_email(token_data.username, session)
        if user is None:
            raise UnauthorizedException()
        return user

    async def authenticate_user(self, email: str, password: str, session: AsyncSession):
        user = await self.user_repository.get_by_email(email, session)

        if not user:
            return False

        is_correct = await self.verify_password(password, user.hashed_password)
        if not is_correct:
            return False

        return user


@lru_cache
def get_AuthService(
    user_repository: Annotated[UserRepository, Depends(get_UserRepository)],
) -> AuthService:
    return AuthService(user_repository)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSessionDep,
    auth_service: Annotated[AuthService, Depends(get_AuthService)],
) -> User:
    return await auth_service.verify_user(token, session)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise UnauthorizedException()
    return current_user


def authorize(role: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user_raw = kwargs.get("current_user")
            current_user: User | None = (
                current_user_raw if isinstance(current_user_raw, User) else None
            )

            if not current_user or not hasattr(current_user, "role"):
                raise UnauthorizedException()

            user_role = current_user.role
            if user_role not in role:
                raise ForbiddenException()

            return await func(*args, **kwargs)

        return wrapper

    return decorator
