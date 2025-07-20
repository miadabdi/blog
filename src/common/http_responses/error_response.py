from enum import StrEnum
from typing import Any

from .base import BaseResponse


class ErrorCodes(StrEnum):
    DUPLICATE_ENTRY = "DUPLICATE_ENTRY"
    ENTITY_NOT_FOUND = "ENTITY_NOT_FOUND"
    NO_CONTENT = "NO_CONTENT"
    INVALID_REQUEST = "INVALID_REQUEST"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    INVALID_TOKEN = "INVALID_TOKEN"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class ErrorResponse(BaseResponse):
    """
    ErrorResponse represents the structure of an error response returned by the API, Inspired by RFC 7807.

    Attributes:
        code (str): A short string representing the error code.
        message (str): A detailed description of the error.
        status (int): The HTTP status code associated with the error.
        timestamp (datetime): The timestamp when the error occurred.
        path (str): The request path that caused the error.
        data (dict[str, Any] | None): Optional additional data related to the error.
    """

    code: ErrorCodes

    # error related data
    detail: list[dict[str, Any]] | dict[str, Any] | None = None
    body: Any | None = None


class ErrorResponseWrapper(ErrorResponse):
    pass
