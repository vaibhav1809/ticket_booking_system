import asyncio
from abc import ABC, abstractmethod

from ..services.seat_lock import ISeatLockService, RedisSeatLockService
from ..db.sessions import redis_client


class IBookingService(ABC):
    @abstractmethod
    async def reserve_seats(self, show_id: str, seat_ids: list[str]) -> None:
        """Reserve seats for a user and return a hold token.

        user: User Information
        Show ID: ID of the show
        seat_ids: List of seat IDs to reserve

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    async def book_seats(
            self,
            user_id: str,
            show_id: str,
            seat_ids: list[str]) -> int:
        """Book seats for a user using a hold token and return a booking ID."""
        raise NotImplementedError


class BookingService(IBookingService):
    __seat_lock_service: ISeatLockService | None = None

    def __init__(self) -> None:
        if self.__seat_lock_service is None:
            self.__seat_lock_service = RedisSeatLockService()

    async def reserve_seats(self, show_id: str, seat_ids: list[str]) -> None:
        """Reserve seats for a user and return a hold token."""

        # create a list of coroutines
        tasks = []
        for seat_id in seat_ids:
            seat_key = f"show:{show_id}:seat:{seat_id}"
            tasks.append(self.__seat_lock_service.lock_seat(seat_key))          # type: ignore

        # trigger all coroutines concurrently
        await asyncio.gather(*tasks)

    async def book_seats(self, user_id: str, show_id: str, seat_ids: list[str]) -> int:
        """Book seats for a user using a hold token and return a booking ID."""
        
        # once the payment system triggers on the webhook we can proceed with booking
        # check if seats are locked
        # update bookings table
        # update tickets table

        # schedule next tasks after booking
        # qr code generatation
        # email sending
        # notifications sending
        # whatsapp message sending

        # return saying booking done

        # if fails return saying could not be done



        return 0
