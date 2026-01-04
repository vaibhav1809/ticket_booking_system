from __future__ import annotations

from typing import Any, Optional, Protocol, Sequence, runtime_checkable
from datetime import datetime

from ..db.models import InventoryStatus, BookingStatus, PaymentStatus


# =====================================================
# Repository Interfaces (ASYNC)
# =====================================================

@runtime_checkable
class IUsersRepo(Protocol):
    async def get(self, user_id: int) -> Any | None: ...
    async def get_by_email(self, email: str) -> Any | None: ...

    async def create(
        self,
        *,
        email_id: str,
        phone: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        password_hash: Optional[bytes] = None,
    ) -> Any: ...


@runtime_checkable
class IEventsRepo(Protocol):
    async def get(self, event_id: int) -> Any | None: ...
    async def create(self, **kwargs: Any) -> Any: ...


@runtime_checkable
class IVenuesRepo(Protocol):
    async def get(self, venue_id: int) -> Any | None: ...


@runtime_checkable
class IShowsRepo(Protocol):
    async def get(self, show_id: int) -> Any | None: ...


@runtime_checkable
class IPricingsRepo(Protocol):
    async def get_for_show(self, show_id: int) -> list[Any]: ...


@runtime_checkable
class IInventoryRepo(Protocol):
    """Seat-level inventory operations (critical for concurrency)."""

    async def lock_for_update(self, *, show_id: int, seat_ids: Sequence[int]) -> list[Any]: ...

    async def mark_booked(
        self,
        *,
        show_id: int,
        seat_ids: Sequence[int],
        booked_by: int) -> int: ...

    async def set_status(
        self,
        *,
        show_id: int,
        seat_ids: Sequence[int],
        status: InventoryStatus,
        booked_by: Optional[int] = None,
    ) -> int: ...


@runtime_checkable
class IBookingsRepo(Protocol):
    async def get(self, booking_id: int) -> Any | None: ...

    async def create(
        self,
        *,
        user_id: int,
        show_id: int,
        status: BookingStatus,
        confirmed_at: Optional[datetime] = None,
    ) -> Any: ...

    async def set_status(
        self,
        *,
        booking_id: int,
        status: BookingStatus,
        confirmed_at: Optional[datetime] = None,
    ) -> None: ...


@runtime_checkable
class IPaymentsRepo(Protocol):
    async def create(
        self,
        *,
        booking_id: int,
        provider: Any,
        status: PaymentStatus,
        amount: int,
        currency: str,
        created_at: datetime,
    ) -> Any: ...

    async def set_status(self, *, payment_id: int, status: PaymentStatus) -> None: ...


@runtime_checkable
class ITicketsRepo(Protocol):
    async def create_many(
        self,
        *,
        booking_id: int,
        show_id: int,
        seat_ids: Sequence[int],
        issued_at: datetime,
    ) -> list[Any]: ...


@runtime_checkable
class IReadsRepo(Protocol):
    """Read-heavy, join-based queries."""

    async def fetch_show_seat_map(self, *, show_id: int) -> list[dict[str, Any]]: ...

    async def fetch_show_details(self, *, show_id: int) -> Optional[dict[str, Any]]: ...


# =====================================================
# Unit of Work Interface (ASYNC ONLY)
# =====================================================

@runtime_checkable
class IAsyncUnitOfWork(Protocol):
    """
    Async Unit of Work contract.

    Responsibilities:
    - Own an AsyncSession
    - Control transaction boundaries
    - Expose repositories bound to the same transaction
    """

    # Wire repos to the same session
    table_users = IUsersRepo
    table_events = IEventsRepo
    table_venues = IVenuesRepo
    table_shows = IShowsRepo
    table_pricing = IPricingsRepo
    table_inventory = IInventoryRepo
    table_bookings = IBookingsRepo
    table_payments = IPaymentsRepo
    table_tickets = ITicketsRepo
    table_read = IReadsRepo

    async def __aenter__(self) -> "IAsyncUnitOfWork": ...
    async def __aexit__(self, exc_type, exc, tb) -> bool: ...

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def close(self) -> None: ...
