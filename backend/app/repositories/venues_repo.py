

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Venue
from .interfaces import IVenuesRepo


class VenuesRepo(IVenuesRepo):
    """Repository for venue operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, venue_id: int) -> Venue | None:
        return await self.session.get(Venue, venue_id)

    async def create(self, **kwargs) -> Venue:
        venue = Venue(**kwargs)
        self.session.add(venue)
        await self.session.flush()  # populate venue_id
        return venue

    async def list(self, *, limit: int = 50, offset: int = 0) -> list[Venue]:
        if hasattr(Venue, "name"):
            stmt = select(Venue).order_by(getattr(Venue, "name")).offset(offset).limit(limit)
        else:
            stmt = select(Venue).order_by(getattr(Venue, "venue_id")).offset(offset).limit(limit)

        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_by_city(self, *, city: str, limit: int = 50) -> list[Venue]:
        if hasattr(Venue, "city"):
            stmt = select(Venue).where(getattr(Venue, "city").ilike(city)).limit(limit)
            res = await self.session.execute(stmt)
            return list(res.scalars().all())

        return []
