
import asyncio
from redis.asyncio import Redis
from abc import ABC, abstractmethod

from ..config import CONFIG
from ..db.sessions import redis_client


class ISeatLockService(ABC):
    def __init__(self, redis_client) -> None:
        self.redis_client = redis_client

    @abstractmethod
    async def lock_seat(self, seat_key: str) -> bool:
        """Lock a seat for a specified TTL (in seconds)."""
        # Implementation goes here
        return True

    @abstractmethod
    async def release_seat(self, seat_key: str) -> None:
        """Release a locked seat."""
        # Implementation goes here
        pass

    @abstractmethod
    async def is_seat_locked(self, seat_key: str) -> bool:
        """Check if a seat is locked."""
        # Implementation goes here
        pass


class RedisSeatLockService(ISeatLockService):
    __client: Redis
    __ttl = None

    def __init__(self) -> None:
        self.__client = redis_client
        self.__ttl = CONFIG.seat_lock_ttl_seconds

    async def lock_seat(self, seat_key: str) -> None:
        """Lock a seat for a specified TTL (in seconds)."""
        if self.__ttl is None:
            raise ValueError("TTL not set for locking a seat.")

        await self.__client.set(seat_key, int(True), ex=self.__ttl)

    async def release_seat(self, seat_key: str) -> None:
        """Release a locked seat."""
        await self.__client.set(seat_key, int(False))

    async def is_seat_locked(self, seat_key: str) -> bool:
        """Check if a seat is locked."""
        val = await self.__client.get(seat_key)
        return bool(val)
