"""
Helpers for OpenAPI documentation of success and error responses.
"""

from typing import Any

from pydantic import BaseModel

from .error_response import ErrorResponseWrapper
from .success_response import SuccessResponse


class ResponseSuccessDoc:
    """
    Helper class for generating OpenAPI documentation for successful responses.
    """

    @staticmethod
    def HTTP_200_OK(description: str, response_type: type[BaseModel]) -> dict:
        return {
            200: {"model": SuccessResponse[response_type], "description": description}
        }

    @staticmethod
    def HTTP_201_CREATED(description: str, response_type: type[BaseModel]) -> dict:
        return {
            201: {"model": SuccessResponse[response_type], "description": description}
        }

    @staticmethod
    def HTTP_202_ACCEPTED(description: str) -> dict:
        return {202: {"model": SuccessResponse, "description": description}}

    @staticmethod
    def HTTP_203_NON_AUTHORITATIVE_INFORMATION(description: str) -> dict:
        return {203: {"model": SuccessResponse, "description": description}}

    @staticmethod
    def HTTP_204_NO_CONTENT(description: str, headers: dict[str, Any]) -> dict:
        return {204: {"description": description, "headers": headers}}


class ResponseErrorDoc:
    """
    Helper class for generating OpenAPI documentation for error responses.
    """

    @staticmethod
    def HTTP_400_BAD_REQUEST(description: str) -> dict:
        return {400: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_401_UNAUTHORIZED(description: str = "Invalid credentials") -> dict:
        return {401: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_402_PAYMENT_REQUIRED(description: str) -> dict:
        return {402: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_403_FORBIDDEN(description: str = "Forbidden") -> dict:
        return {403: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_404_NOT_FOUND(description: str = "Entity not found") -> dict:
        return {404: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_405_METHOD_NOT_ALLOWED(description: str) -> dict:
        return {405: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_409_CONFLICT(description: str = "Conflict") -> dict:
        return {409: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_429_TOO_MANY_REQUESTS(description: str) -> dict:
        return {429: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_422_UNPROCESSABLE_ENTITY(description: str) -> dict:
        return {422: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_498_INVALID_TOKEN(description: str) -> dict:
        return {498: {"model": ErrorResponseWrapper, "description": description}}

    @staticmethod
    def HTTP_500_INTERNAL_SERVER_ERROR(description: str = "Internal Exception") -> dict:
        return {500: {"model": ErrorResponseWrapper, "description": description}}
