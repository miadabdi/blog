import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .custom_base_exception import CustomBaseException

logger = logging.getLogger(__name__)


class ForbiddenException(CustomBaseException):
    def __init__(
        self,
        message: str = "Forbidden. You do not have permission to access this resource.",
    ):
        super().__init__(message=message)


async def forbidden_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.debug(
        exc.message if isinstance(exc, CustomBaseException) else str(exc),
    )

    if not isinstance(exc, ForbiddenException):
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred."},
        )

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "message": exc.message
            if isinstance(exc, CustomBaseException)
            else "Forbidden."
        },
    )
