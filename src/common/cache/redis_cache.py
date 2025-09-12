import json
from typing import Any, Optional

from ..exceptions.exceptions import InternalException

from .base import CacheInterface


class RedisCache(CacheInterface):
    """Asynchronous Redis cache wrapper with lazy import.

    The redis.asyncio module is imported lazily inside connect() so that
    importing this module does not fail in environments where the redis
    package is not installed (e.g., during some unit tests).
    """

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client: Optional[Any] = None
        self._redis_module: Optional[Any] = None

    async def connect(self):
        if not self.client:
            try:
                # Import redis.asyncio lazily to avoid import-time failures
                if self._redis_module is None:
                    import importlib

                    self._redis_module = importlib.import_module("redis.asyncio")

                self.client = self._redis_module.from_url(self.redis_url)
            except Exception as e:
                raise InternalException(
                    message="Failed to connect to Redis cache", underlying_error=e
                )

    async def get(self, key: str) -> Optional[Any]:
        await self.connect()
        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            raise InternalException(
                message=f"Failed to get cache key: {key}", underlying_error=e
            )

    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        await self.connect()
        try:
            await self.client.set(key, json.dumps(value, default=str), ex=expire)
        except Exception as e:
            raise InternalException(
                message=f"Failed to set cache key: {key}", underlying_error=e
            )

    async def delete(self, key: str) -> None:
        await self.connect()
        try:
            await self.client.delete(key)
        except Exception as e:
            raise InternalException(
                message=f"Failed to delete cache key: {key}", underlying_error=e
            )

    async def exists(self, key: str) -> bool:
        await self.connect()
        try:
            return bool(await self.client.exists(key))
        except Exception as e:
            raise InternalException(
                message=f"Failed to check cache key existence: {key}",
                underlying_error=e,
            )

    async def close(self) -> None:
        if self.client:
            await self.client.close()