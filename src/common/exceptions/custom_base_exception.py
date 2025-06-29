import logging

from fastapi import Request
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomBaseException(Exception):
    def __init__(self, message: str):
        self.message = message


async def custom_base_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.debug(
        exc.message if isinstance(exc, CustomBaseException) else str(exc),
    )

    if not isinstance(exc, CustomBaseException):
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred."},
        )

    return JSONResponse(
        status_code=500,
        content={"message": exc.message or "An unexpected error occurred."},
    )
