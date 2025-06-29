import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .custom_base_exception import CustomBaseException

logger = logging.getLogger(__name__)


class ConflictException(CustomBaseException):
    def __init__(
        self, resource: str, message: str = "Resource conflict or uniqueness violation."
    ):
        self.resource = resource
        super().__init__(message=message)


async def conflict_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.debug(
        exc.message if isinstance(exc, CustomBaseException) else str(exc),
    )

    if not isinstance(exc, ConflictException):
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred."},
        )

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": f"{exc.message} for {exc.resource}."},
    )
