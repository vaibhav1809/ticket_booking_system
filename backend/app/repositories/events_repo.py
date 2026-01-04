

from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Event
from .interfaces import IEventsRepo


class EventsRepo(IEventsRepo):
    """Repository for event operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, event_id: int) -> Event | None:
        return await self.session.get(Event, event_id)

    async def create(self, **kwargs) -> Event:
        event = Event(**kwargs)
        self.session.add(event)
        await self.session.flush()  # populate event_id
        return event

    async def list(self, *, limit: int = 50, offset: int = 0) -> list[Event]:
        # Prefer created_at if the model has it
        if hasattr(Event, "created_at"):
            stmt = select(Event).order_by(
                desc(getattr(Event, "created_at"))).offset(offset).limit(limit)
        else:
            stmt = select(Event).order_by(
                desc(getattr(Event, "event_id"))).offset(offset).limit(limit)

        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def search_by_title(self, *, query: str, limit: int = 20) -> list[Event]:
        # Use ILIKE if supported by the backend (Postgres). SQLAlchemy will translate appropriately.
        if hasattr(Event, "title"):
            stmt = select(Event).where(getattr(Event, "title").ilike(f"%{query}%")).limit(limit)
        else:
            # Fallback: no title column
            stmt = select(Event).limit(0)

        res = await self.session.execute(stmt)
        return list(res.scalars().all())
