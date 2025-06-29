from .conflict import (
    ConflictException,
    conflict_exception_handler,
)
from .custom_base_exception import CustomBaseException, custom_base_exception_handler
from .forbidden import (
    ForbiddenException,
    forbidden_exception_handler,
)
from .internal import (
    InternalException,
    internal_exception_handler,
)
from .invalid_credintials import (
    InvalidCredentialsException,
    invalid_credentials_exception_handler,
)
from .not_found import NotFoundException, not_found_exception_handler
from .unauthorized import (
    UnauthorizedException,
    unauthorized_exception_handler,
)


def register_exceptions(app):
    """
    Register custom exception handlers for the FastAPI application.
    """
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(
        InvalidCredentialsException, invalid_credentials_exception_handler
    )
    app.add_exception_handler(ConflictException, conflict_exception_handler)
    app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
    app.add_exception_handler(InternalException, internal_exception_handler)
    app.add_exception_handler(
        CustomBaseException, custom_base_exception_handler
    )  # Catch-all for other exceptions
