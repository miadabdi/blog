import datetime

from ...configure_logging import logging
from ..http_responses.error_response import ErrorCodes, ErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppBaseException(Exception):
    def __init__(
        self,
        *,
        code: ErrorCodes = ErrorCodes.INTERNAL_SERVER_ERROR,
        message: str = "An unexpected error occurred.",
        status_code: int = 500,
        data: dict | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data or {}

    def to_response_model(self, path: str = "") -> ErrorResponse:
        return ErrorResponse(
            # type=f"https://api.example.com/errors/{self.code.value.lower()}", !# not needed for now
            code=self.code,
            message=self.message,
            status=self.status_code,
            timestamp=datetime.datetime.now(
                datetime.timezone.utc
            ),  # RFC 3339-compliant
            path=path,
            data=self.data,
        )


class DatabaseOperationException(AppBaseException):
    def __init__(
        self,
        operation: str | None = None,
        message: str | None = None,
        data: dict | None = None,
    ):
        message = f"Failed to perform {operation} operation. {message} "

        super().__init__(
            code=ErrorCodes.DATABASE_ERROR,
            message=message,
            status_code=500,
            data=data,
        )


class InvalidTokenException(AppBaseException):
    """Raised when ."""

    def __init__(self, message="Invalid token", token: str = "No token provided"):
        super().__init__(
            code=ErrorCodes.INVALID_TOKEN,
            message=message,
            status_code=401,
            data={"token": token},
        )


class InvalidPayloadException(AppBaseException):
    """Raised when ."""

    def __init__(self, message="Invalid payload", payload=None):
        super().__init__(
            code=ErrorCodes.INVALID_PAYLOAD,
            message=message,
            status_code=401,
            data={"payload": payload},
        )
        if payload is None:
            payload = {1: "No payload provided"}


class DuplicateEntryException(AppBaseException):
    def __init__(self, field: str, resource: str, value: str | None = None):
        super().__init__(
            code=ErrorCodes.DUPLICATE_ENTRY,
            message=f"{field} '{value}' already exists in resource {resource}.",
            status_code=409,
            data={field: value},
        )


class EntityNotFoundException(AppBaseException):
    def __init__(self, resource: str | None = None, resource_id: str | None = None):
        self.resource = resource
        self.resource_id = resource_id
        data = {"identifier": resource_id}
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
            data=data,
        )


class InvalidCredentialsException(AppBaseException):
    def __init__(self, data=None, message: str = "Authentication failed"):
        if data is None:
            data = {}
        super().__init__(
            code=ErrorCodes.INVALID_CREDENTIALS,
            message=message,
            status_code=401,
            data=data,
        )


class UnauthorizedException(AppBaseException):
    def __init__(self, data=None, message: str = "Unauthorized"):
        if data is None:
            data = {}
        super().__init__(
            code=ErrorCodes.UNAUTHORIZED,
            message=message,
            status_code=401,
            data=data,
        )


class ForbiddenException(AppBaseException):
    def __init__(
        self,
        data=None,
        message: str = "Forbidden. You do not have permission to access this resource.",
    ):
        if data is None:
            data = {}
        super().__init__(
            code=ErrorCodes.FORBIDDEN,
            message=message,
            status_code=403,
            data=data,
        )


class InternalException(AppBaseException):
    def __init__(
        self,
        *,
        code: ErrorCodes = ErrorCodes.INTERNAL_SERVER_ERROR,
        message: str = "An unexpected error occurred.",
        status_code: int = 500,
        data: dict | None = None,
        underlying_error: Exception | None = None,
    ):
        logger.debug(
            underlying_error.message
            if isinstance(underlying_error, AppBaseException)
            else str(underlying_error),
        )
        super().__init__(code=code, message=message, status_code=status_code, data=data)
