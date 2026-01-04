

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import (
    Event,
    Inventory,
    Show,
    ShowPricing,
    Venue,
    VenueSeat,
    VenueSection,
)
from .interfaces import IReadsRepo


class ReadsRepo(IReadsRepo):
    """Read-heavy, join-based queries.

    These queries intentionally return dictionaries instead of ORM objects
    to avoid accidental writes and keep the read layer lightweight.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def fetch_show_seat_map(self, *, show_id: int) -> list[dict[str, Any]]:
        """Return seat map for a show with section, pricing and inventory status."""

        stmt = (
            select(
                VenueSeat.seat_id,
                VenueSeat.row_nums,
                VenueSeat.col_nums,
                VenueSection.section_id,
                VenueSection.name.label("section_name"),
                ShowPricing.amount.label("price"),
                ShowPricing.currency,
                Inventory.status.label("inventory_status"),
            )
            .select_from(Inventory)
            .join(VenueSeat, VenueSeat.seat_id == Inventory.seat_id)
            .join(VenueSection, VenueSection.section_id == VenueSeat.section_id)
            .join(
                ShowPricing,
                (ShowPricing.show_id == Inventory.show_id)
                & (ShowPricing.section_id == VenueSection.section_id),
            )
            .where(Inventory.show_id == show_id)
            .order_by(VenueSection.order, VenueSeat.row_nums, VenueSeat.col_nums)
        )

        rows = (await self.session.execute(stmt)).mappings().all()
        return [dict(r) for r in rows]

    async def fetch_show_details(self, *, show_id: int) -> dict[str, Any] | None:
        """Return show + event + venue details."""

        stmt = (
            select(
                Show.show_id,
                Show.start_time,
                Show.end_time,
                Show.status.label("show_status"),
                Event.event_id,
                Event.title.label("event_title"),
                Event.event_type,
                Venue.venue_id,
                Venue.name.label("venue_name"),
                Venue.city,
            )
            .join(Event, Event.event_id == Show.event_id)
            .join(Venue, Venue.venue_id == Show.venue_id)
            .where(Show.show_id == show_id)
        )

        row = (await self.session.execute(stmt)).mappings().first()
        return dict(row) if row else None


# Backwards-compatible alias in case other modules import ReadRepo
# ReadRepo = ReadsRepo()
