import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .custom_base_exception import CustomBaseException

logger = logging.getLogger(__name__)


class UnauthorizedException(CustomBaseException):
    def __init__(self, message: str = "Unauthorized access."):
        super().__init__(message=message)


async def unauthorized_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.debug(
        exc.message if isinstance(exc, CustomBaseException) else str(exc),
    )

    if not isinstance(exc, UnauthorizedException):
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred."},
        )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message": exc.message
            if isinstance(exc, CustomBaseException)
            else "Unauthorized."
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
