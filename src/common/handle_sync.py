from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

from fastapi.concurrency import run_in_threadpool

from .exceptions.internal import InternalException

P = ParamSpec("P")
T = TypeVar("T")


def _handle_sync(func: Callable[P, T]) -> Callable[P, Awaitable[T]]:
    """Decorator to make underlying func async."""

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await run_in_threadpool(func, *args, **kwargs)
        except Exception as e:
            raise InternalException(message=f"Unexpected error in {func.__name__}: {e}")

    return wrapper
