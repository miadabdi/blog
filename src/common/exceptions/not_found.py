import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .custom_base_exception import CustomBaseException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotFoundException(CustomBaseException):
    def __init__(self, resource: str | None = None, resource_id: str | None = None):
        self.resource = resource
        message = (
            f"{resource} with id {resource_id} not found."
            if resource and resource_id
            else f"{resource} not found."
            if resource
            else "Resource not found."
        )
        super().__init__(message=message)


async def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.debug(
        exc.message if isinstance(exc, CustomBaseException) else str(exc),
    )

    if not isinstance(exc, NotFoundException):
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred."},
        )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": f"{exc.resource} not found."
            if exc.resource
            else "Resource not found."
        },
    )
