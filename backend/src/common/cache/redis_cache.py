import json
from typing import Any, Optional

import redis.asyncio as redis

from ..exceptions.exceptions import InternalException
from .base import CacheInterface


class RedisCache(CacheInterface):
    """Asynchronous Redis cache wrapper with eager import.

    The redis.asyncio module is imported at module import time, so ensure the
    'redis' package is installed in your environment.
    """

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client: Optional[redis.Redis] = None

    async def connect(self):
        if not self.client:
            try:
                # Create an async Redis client using the eagerly imported module
                self.client = redis.from_url(self.redis_url)
            except Exception as e:
                raise InternalException(
                    message="Failed to connect to Redis cache", underlying_error=e
                )

    async def get(self, key: str) -> Optional[Any]:
        await self.connect()
        client = self.client
        if client is None:
            raise InternalException(message="Redis client not initialized")
        try:
            value = await client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            raise InternalException(
                message=f"Failed to get cache key: {key}", underlying_error=e
            )

    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        await self.connect()
        client = self.client
        if client is None:
            raise InternalException(message="Redis client not initialized")
        try:
            await client.set(key, json.dumps(value, default=str), ex=expire)
        except Exception as e:
            raise InternalException(
                message=f"Failed to set cache key: {key}", underlying_error=e
            )

    async def delete(self, key: str) -> None:
        await self.connect()
        client = self.client
        if client is None:
            raise InternalException(message="Redis client not initialized")
        try:
            await client.delete(key)
        except Exception as e:
            raise InternalException(
                message=f"Failed to delete cache key: {key}", underlying_error=e
            )

    async def exists(self, key: str) -> bool:
        await self.connect()
        client = self.client
        if client is None:
            raise InternalException(message="Redis client not initialized")
        try:
            return bool(await client.exists(key))
        except Exception as e:
            raise InternalException(
                message=f"Failed to check cache key existence: {key}",
                underlying_error=e,
            )

    async def close(self) -> None:
        if self.client:
            await self.client.close()
