from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Booking, BookingStatus
from .interfaces import IBookingsRepo


class BookingsRepo(IBookingsRepo):
    """Repository for booking operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, booking_id: int) -> Optional[Booking]:
        return await self.session.get(Booking, booking_id)

    async def create(
        self,
        *,
        user_id: int,
        show_id: int,
        status: BookingStatus,
        confirmed_at: Optional[datetime] = None,
    ) -> Booking:
        booking = Booking(
            user_id=user_id,
            show_id=show_id,
            status=status,
            confirmed_at=confirmed_at,
        )
        self.session.add(booking)
        await self.session.flush()  # populate booking_id
        return booking

    async def set_status(
        self,
        *,
        booking_id: int,
        status: BookingStatus,
        confirmed_at: Optional[datetime] = None,
    ) -> None:
        stmt = (
            update(Booking)
            .where(Booking.booking_id == booking_id)
            .values(status=status, confirmed_at=confirmed_at)
        )
        await self.session.execute(stmt)
