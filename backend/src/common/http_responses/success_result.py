"""
SuccessResult dataclass for wrapping successful API responses.
"""

import datetime
from dataclasses import dataclass
from typing import Generic, TypeVar

from fastapi import Request
from fastapi.responses import JSONResponse

from .success_response import SuccessCodes, SuccessResponse

T = TypeVar("T")


@dataclass
class SuccessResult(Generic[T]):
    """
    Wrapper for successful API responses.

    Args:
        code (SuccessCodes): Success code.
        message (str): Success message.
        status_code (int): HTTP status code.
        data (T | None): Response data.

    Methods:
        to_response_model(path: str) -> SuccessResponse[T]:
            Convert to a SuccessResponse model.
        to_json_response(request: Request) -> JSONResponse:
            Convert to a FastAPI JSONResponse.
    """

    def __init__(
        self,
        *,
        code: SuccessCodes = SuccessCodes.SUCCESS,
        message: str = "Operation successful",
        status_code: int = 200,
        data: T | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data

    def to_response_model(self, path: str) -> SuccessResponse[T]:
        """
        Convert to a SuccessResponse model.

        Args:
            path (str): The request path.

        Returns:
            SuccessResponse[T]: The response model.
        """
        return SuccessResponse[T](
            code=self.code,
            message=self.message,
            status=self.status_code,
            data=self.data,
            timestamp=datetime.datetime.now(
                datetime.timezone.utc
            ),  # RFC 3339-compliant
            path=path,
        )

    def to_json_response(self, request: Request) -> JSONResponse:
        """
        Convert to a FastAPI JSONResponse.

        Args:
            request (Request): The FastAPI request.

        Returns:
            JSONResponse: The JSON response.
        """
        model = self.to_response_model(path=request.url.path)
        return JSONResponse(
            status_code=self.status_code,
            content=model.model_dump(mode="json"),
        )
