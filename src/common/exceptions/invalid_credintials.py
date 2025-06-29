import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .custom_base_exception import CustomBaseException

logger = logging.getLogger(__name__)


class InvalidCredentialsException(CustomBaseException):
    def __init__(self, message: str = "Invalid credentials provided."):
        super().__init__(
            message=message,
        )


async def invalid_credentials_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.debug(
        exc.message if isinstance(exc, CustomBaseException) else str(exc),
    )

    if not isinstance(exc, InvalidCredentialsException):
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred."},
        )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": exc.message
            if isinstance(exc, CustomBaseException)
            else "Invalid credentials provided."
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
