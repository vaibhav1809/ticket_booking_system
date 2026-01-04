

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Show
from .interfaces import IShowsRepo


class ShowsRepo(IShowsRepo):
    """Repository for `shows` table operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, show_id: int) -> Show | None:
        return await self.session.get(Show, show_id)

    async def list_by_event(self, event_id: int) -> list[Show]:
        stmt = select(Show).where(Show.event_id == event_id).order_by(Show.start_time)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_by_venue(self, venue_id: int) -> list[Show]:
        stmt = select(Show).where(Show.venue_id == venue_id).order_by(Show.start_time)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_upcoming(self, *, now: datetime | None = None, limit: int = 50) -> list[Show]:
        """Return upcoming shows ordered by start time."""
        now = now or datetime.utcnow()
        stmt = (
            select(Show)
            .where(Show.start_time >= now)
            .order_by(Show.start_time)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
