from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import AppBaseException


async def handle_app_exception(
    request: Request, exc: Union[Exception, AppBaseException]
) -> JSONResponse:
    # Cast to AppBaseException since we know it will be that type when called
    app_exc = exc if isinstance(exc, AppBaseException) else AppBaseException()
    error_model = app_exc.to_response_model(path=request.url.path)
    return JSONResponse(
        status_code=app_exc.status_code,
        content={"detail": error_model.model_dump(mode="json")},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppBaseException, handle_app_exception)
