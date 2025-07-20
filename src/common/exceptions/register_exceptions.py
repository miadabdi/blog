import datetime
from typing import Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..http_responses.error_response import ErrorCodes, ErrorResponse
from .exceptions import AppBaseException


async def handle_app_exception(
    request: Request, exc: Union[Exception, AppBaseException]
) -> JSONResponse:
    # Cast to AppBaseException since we know it will be that type when called
    app_exc = exc if isinstance(exc, AppBaseException) else AppBaseException()
    error_model = app_exc.to_response_model(request)
    return JSONResponse(
        status_code=app_exc.status_code,
        content=error_model.model_dump(mode="json"),
    )


async def validation_exception_handler(
    request: Request, exc: Union[Exception, RequestValidationError]
):
    # Cast to AppBaseException since we know it will be that type when called
    validation_exc = (
        exc
        if isinstance(exc, RequestValidationError)
        else RequestValidationError(exc.errors())  # type: ignore[call-arg]
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            code=ErrorCodes.VALIDATION_ERROR,
            message="Validation error",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            timestamp=datetime.datetime.now(
                datetime.timezone.utc
            ),  # RFC 3339-compliant
            path=request.url.path,
            detail=list(validation_exc.errors()),
            body=validation_exc.body,
        ).model_dump(mode="json"),
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppBaseException, handle_app_exception)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
