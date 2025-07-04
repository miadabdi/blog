import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .custom_base_exception import CustomBaseException

logger = logging.getLogger(__name__)


class InternalException(CustomBaseException):
    def __init__(
        self,
        message: str = "Internal server error.",
        underlying_error: Exception | None = None,
    ):
        self.underlying_error = underlying_error
        super().__init__(message=message)


async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        exc.message if isinstance(exc, CustomBaseException) else str(exc),
        exc,
        exc_info=True,
    )

    if not isinstance(exc, InternalException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred."},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error."},
    )
