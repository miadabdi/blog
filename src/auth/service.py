from datetime import timedelta
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from ..common.settings import settings
from .auth import AuthService, get_AuthService
from .models import User
from .repository import UserRepository, get_UserRepository
from .schemas import SignUp, Token, UpdateUser


class UserService:
    def __init__(self, auth_service: AuthService, user_repository: UserRepository):
        self.repository = user_repository
        self.auth_service = auth_service

    async def create_user(self, data: User, session: AsyncSession) -> User:
        user_record = await self.repository.create(data.model_dump(), session)
        await session.commit()
        return user_record

    async def sign_up(self, form_data: SignUp, session: AsyncSession):
        dup = await self.get_user_by_email(form_data.email, session)
        if dup:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email Already Exists",
            )

        hashed_password = await self.auth_service.get_password_hash(form_data.password)
        user = User(**form_data.model_dump(), hashed_password=hashed_password)

        await self.create_user(user, session)
        await session.commit()

        return {"message": "ok"}

    async def sign_in(
        self, form_data: OAuth2PasswordRequestForm, session: AsyncSession
    ):
        user = await self.auth_service.authenticate_user(
            form_data.username, form_data.password, session
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        await session.commit()
        return Token(access_token=access_token, token_type="bearer")

    async def update_user(
        self, id: int, update_data: UpdateUser, session: AsyncSession
    ) -> User:
        user_data = update_data.model_dump(exclude_unset=True)
        updated_user = await self.repository.update(id, user_data, session)
        await session.commit()

        return updated_user

    async def delete_user(self, id: int, session: AsyncSession) -> User:
        result = await self.repository.delete(id, session)
        await session.commit()
        return result

    async def get_user_by_id(self, id: int, session: AsyncSession) -> User | None:
        result = await self.repository.get_by_id(id, session)
        await session.commit()
        return result

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        result = await self.repository.get_by_email(email, session)
        await session.commit()
        return result


@lru_cache
def get_UserService(
    auth_service: Annotated[AuthService, Depends(get_AuthService)],
    user_repository: Annotated[UserRepository, Depends(get_UserRepository)],
) -> UserService:
    return UserService(auth_service, user_repository)
