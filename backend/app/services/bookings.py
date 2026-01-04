import asyncio
from abc import ABC, abstractmethod

from ..services.seat_lock import ISeatLockService, RedisSeatLockService
from ..db.sessions import redis_client
from datetime import datetime, timezone
from ..repositories.uow import AsyncUnitOfWork
from ..db.models import BookingStatus, InventoryStatus, PaymentStatus


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
        """Book seats for a user and return a booking ID.

        MVP behavior:
        - Assumes payment success (dummy)
        - Uses a single DB transaction via AsyncUnitOfWork
        - Releases Redis locks only AFTER a successful DB commit
        """

        # --- Basic validation / parsing ---
        if not seat_ids:
            raise ValueError("seat_ids cannot be empty")

        try:
            user_id_int = int(user_id)
            show_id_int = int(show_id)
            seat_id_ints = [int(s) for s in seat_ids]
        except ValueError as e:
            raise ValueError("user_id/show_id/seat_ids must be numeric strings") from e

        # once the payment system triggers on the webhook we can proceed with booking
        payment_successful = True
        if not payment_successful:
            raise RuntimeError("Payment failed")

        # Redis keys for locks (release only after commit)
        lock_keys = [f"show:{show_id}:seat:{seat_id}" for seat_id in seat_ids]

        # Dummy pricing for now (replace with pricing lookup later)
        price_per_seat = 250
        total_amount = price_per_seat * len(seat_id_ints)
        currency = "INR"
        now = datetime.now(timezone.utc)

        booking_id: int

        async with AsyncUnitOfWork() as uow:
            # 1) Concurrency-safe lock on inventory rows
            # we need to check with the (show_id + seat_id) as the primary_key
            locked_rows = await uow.table_inventory.lock_for_update(show_id=show_id_int, seat_ids=seat_id_ints)

            if len(locked_rows) != len(seat_id_ints):
                raise RuntimeError("One or more seats not found in inventories")

            unavailable = [r.seat_id for r in locked_rows if r.status != InventoryStatus.available]
            if unavailable:
                raise RuntimeError(f"Some seats are not available: {unavailable}")

            # 2) Create booking (confirmed)
            booking = await uow.table_bookings.create(
                user_id=user_id_int,
                show_id=show_id_int,
                status=BookingStatus.confirmed,
                confirmed_at=now,
            )
            booking_id = int(booking.booking_id)

            # 3) Create payment (success) - dummy provider for now
            await uow.table_payments.create(
                booking_id=booking_id,
                provider="upi",
                status=PaymentStatus.success,
                amount=total_amount,
                currency=currency,
                created_at=now,
            )

            # 4) Mark inventories booked
            updated = await uow.table_inventory.mark_booked(
                show_id=show_id_int, seat_ids=seat_id_ints, booked_by=user_id_int)
            if updated != len(seat_id_ints):
                raise RuntimeError(
                    f"Inventory update mismatch: updated {updated}, expected {len(seat_id_ints)}")

            # 5) Create tickets
            await uow.table_tickets.create_many(
                booking_id=booking_id,
                show_id=show_id_int,
                seat_ids=seat_id_ints,
                issued_at=now,
            )

            # 6) Commit all changes
            await uow.commit()

        # Release seat locks from redis ONLY after DB commit succeeded
        if lock_keys:
            await redis_client.delete(*lock_keys)  # type: ignore

        return booking_id
