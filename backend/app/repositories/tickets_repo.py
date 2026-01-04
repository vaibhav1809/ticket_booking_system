

from __future__ import annotations

import secrets
from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Ticket
from .interfaces import ITicketsRepo


class TicketsRepo(ITicketsRepo):
    """Repository for ticket operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(
        self,
        *,
        booking_id: int,
        show_id: int,
        seat_ids: Sequence[int],
        issued_at: datetime,
    ) -> list[Ticket]:
        tickets: list[Ticket] = []

        # TicketStatus is optional depending on your models.py
        TicketStatus = getattr(
            __import__(
                "app.db.models",
                fromlist=["TicketStatus"]),
            "TicketStatus",
            None)
        active_status = getattr(TicketStatus, "active", None) if TicketStatus else None

        for seat_id in seat_ids:
            t = Ticket(
                booking_id=booking_id,
                show_id=show_id,
                seat_id=seat_id,
                ticket_code=secrets.token_urlsafe(10)[:20],
                issued_at=issued_at,
            )
            if active_status is not None and hasattr(t, "status"):
                setattr(t, "status", active_status)
            tickets.append(t)

        self.session.add_all(tickets)
        await self.session.flush()              # populate ticket_id(s)
        return tickets
