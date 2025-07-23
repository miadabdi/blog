"""
Custom exception classes for application errors.
"""

import datetime

from fastapi import Request

from ...configure_logging import logging
from ..http_responses.error_response import ErrorCodes, ErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppBaseException(Exception):
    """
    Base exception for application errors.

    Args:
        code (ErrorCodes): Error code.
        message (str): Error message.
        status_code (int): HTTP status code.
        detail (dict | None): Additional error details.
    """

    def __init__(
        self,
        *,
        code: ErrorCodes = ErrorCodes.INTERNAL_SERVER_ERROR,
        message: str = "An unexpected error occurred.",
        status_code: int = 500,
        detail: dict | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}

    def to_response_model(self, request: Request) -> ErrorResponse:
        """
        Convert to an ErrorResponse model.

        Args:
            request (Request): The FastAPI request.

        Returns:
            ErrorResponse: The error response model.
        """
        return ErrorResponse(
            # type=f"https://api.example.com/errors/{self.code.value.lower()}", !# not needed for now
            code=self.code,
            message=self.message,
            status=self.status_code,
            timestamp=datetime.datetime.now(
                datetime.timezone.utc
            ),  # RFC 3339-compliant
            path=request.url.path,
            detail=self.detail,
        )


class DatabaseOperationException(AppBaseException):
    """
    Exception for database operation errors.
    """

    def __init__(
        self,
        operation: str | None = None,
        message: str | None = None,
        detail: dict | None = None,
    ):
        message = f"Failed to perform {operation} operation. {message} "

        super().__init__(
            code=ErrorCodes.DATABASE_ERROR,
            message=message,
            status_code=500,
            detail=detail,
        )


class InvalidTokenException(AppBaseException):
    """
    Exception for invalid token errors.
    """

    def __init__(self, message="Invalid token", token: str = "No token provided"):
        super().__init__(
            code=ErrorCodes.INVALID_TOKEN,
            message=message,
            status_code=401,
            detail={"token": token},
        )


class InvalidPayloadException(AppBaseException):
    """
    Exception for invalid payload errors.
    """

    def __init__(self, message="Invalid payload", payload=None):
        super().__init__(
            code=ErrorCodes.INVALID_PAYLOAD,
            message=message,
            status_code=401,
            detail={"payload": payload},
        )
        if payload is None:
            payload = {1: "No payload provided"}


class DuplicateEntryException(AppBaseException):
    """
    Exception for duplicate entry errors.
    """

    def __init__(self, field: str, resource: str, value: str | None = None):
        super().__init__(
            code=ErrorCodes.DUPLICATE_ENTRY,
            message=f"{field} '{value}' already exists in resource {resource}.",
            status_code=409,
            detail={field: value},
        )


class EntityNotFoundException(AppBaseException):
    """
    Exception for entity not found errors.
    """

    def __init__(self, resource: str | None = None, resource_id: str | None = None):
        self.resource = resource
        self.resource_id = resource_id
        detail = {"identifier": resource_id}
        message = (
            f"{resource} with id {resource_id} not found."
            if resource and resource_id
            else f"{resource} not found."
            if resource
            else "Resource not found."
        )

        super().__init__(
            code=ErrorCodes.ENTITY_NOT_FOUND,
            message=message,
            status_code=404,
            detail=detail,
        )


class InvalidCredentialsException(AppBaseException):
    """
    Exception for invalid credentials errors.
    """

    def __init__(self, detail=None, message: str = "Authentication failed"):
        if detail is None:
            detail = {}
        super().__init__(
            code=ErrorCodes.INVALID_CREDENTIALS,
            message=message,
            status_code=401,
            detail=detail,
        )


class UnauthorizedException(AppBaseException):
    """
    Exception for unauthorized access errors.
    """

    def __init__(self, detail=None, message: str = "Unauthorized"):
        if detail is None:
            detail = {}
        super().__init__(
            code=ErrorCodes.UNAUTHORIZED,
            message=message,
            status_code=401,
            detail=detail,
        )


class ForbiddenException(AppBaseException):
    """
    Exception for forbidden access errors.
    """

    def __init__(
        self,
        detail=None,
        message: str = "Forbidden. You do not have permission to access this resource.",
    ):
        if detail is None:
            detail = {}
        super().__init__(
            code=ErrorCodes.FORBIDDEN,
            message=message,
            status_code=403,
            detail=detail,
        )


class InternalException(AppBaseException):
    """
    Exception for unexpected internal errors.

    Args:
        code (ErrorCodes): Error code.
        message (str): Error message.
        status_code (int): HTTP status code.
        detail (dict | None): Additional error details.
        underlying_error (Exception | None): The underlying exception.
    """

    def __init__(
        self,
        *,
        code: ErrorCodes = ErrorCodes.INTERNAL_SERVER_ERROR,
        message: str = "An unexpected error occurred.",
        status_code: int = 500,
        detail: dict | None = None,
        underlying_error: Exception | None = None,
    ):
        logger.debug(
            underlying_error.message
            if isinstance(underlying_error, AppBaseException)
            else str(underlying_error),
        )
        super().__init__(
            code=code, message=message, status_code=status_code, detail=detail
        )
