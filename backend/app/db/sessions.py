import sys
from typing import Optional

from redis.asyncio import Redis

from ..config import log, CONFIG

__all__ = ["redis_client"]


class RedisClient:
    _client: Optional[Redis] = None

    @classmethod
    def get_client(cls) -> Redis:
        if cls._client is None:
            if CONFIG.redis_host is None or CONFIG.redis_port is None:
                log.error("Redis configuration is missing.")
                sys.exit(1)

            cls._client = Redis(
                host=CONFIG.redis_host,
                port=CONFIG.redis_port,
                password=CONFIG.redis_password,
                decode_responses=True,
            )
        return cls._client


redis_client: Redis = RedisClient.get_client()
