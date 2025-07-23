"""
Exception handler registration for FastAPI.
Provides global exception handling for custom and validation errors.
"""

import datetime

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..http_responses.error_response import ErrorCodes, ErrorResponse
from .exceptions import AppBaseException


async def handle_app_exception(request: Request, exc: AppBaseException):
    """
    Handle custom application exceptions.

    Args:
        request (Request): The FastAPI request.
        exc (AppBaseException): The custom exception.

    Returns:
        JSONResponse: The error response.
    """
    error_model = exc.to_response_model(request)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_model.model_dump(mode="json"),
    )


async def handle_validation_exception(request: Request, exc: RequestValidationError):
    """
    Handle validation errors.

    Args:
        request (Request): The FastAPI request.
        exc (RequestValidationError): The validation exception.

    Returns:
        JSONResponse: The error response.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            code=ErrorCodes.VALIDATION_ERROR,
            message="Validation error",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            path=request.url.path,
            detail=list(exc.errors()),
            body=exc.body,
        ).model_dump(mode="json"),
    )


async def handle_internal_exception(request: Request, exc: Exception):
    """
    Handle unexpected internal exceptions.

    Args:
        request (Request): The FastAPI request.
        exc (Exception): The exception.

    Returns:
        JSONResponse: The error response.
    """
    internal_exc = AppBaseException(detail={"message": str(exc)})
    return await handle_app_exception(request, internal_exc)


async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for FastAPI.

    Args:
        request (Request): The FastAPI request.
        exc (Exception): The exception.

    Returns:
        JSONResponse: The error response.
    """
    if isinstance(exc, AppBaseException):
        return await handle_app_exception(request, exc)
    elif isinstance(exc, RequestValidationError):
        return await handle_validation_exception(request, exc)
    else:
        return await handle_internal_exception(request, exc)


def register_exception_handlers(app: FastAPI):
    """
    Register global exception handlers for FastAPI.

    Args:
        app (FastAPI): The FastAPI application.
    """
    app.add_exception_handler(Exception, global_exception_handler)
    # weirdly, this is needed to handle validation errors globally
    app.add_exception_handler(RequestValidationError, global_exception_handler)
