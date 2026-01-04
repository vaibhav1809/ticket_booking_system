"""Async Unit-of-Work (UoW) for SQLAlchemy AsyncSession.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .interfaces import IAsyncUnitOfWork

# Repo implementations (you said these are already separated)
from .users_repo import UsersRepo
from .events_repo import EventsRepo
from .venues_repo import VenuesRepo
from .shows_repo import ShowsRepo
from .pricings_repo import PricingsRepo
from .inventory_repo import InventoryRepo
from .bookings_repo import BookingsRepo
from .payments_repo import PaymentsRepo
from .tickets_repo import TicketsRepo
from .reads_repo import ReadsRepo


class RepositoryError(Exception):
    """Wraps DB constraint/transaction errors into a single exception type."""


def _make_async_engine() -> AsyncEngine:
    url = os.getenv(
        "DATABASE_URL") or "postgresql+asyncpg://postgres:postgres@localhost:5432/ticketing"

    parsed = make_url(url)
    if not parsed.drivername.endswith("+asyncpg"):
        raise ValueError("DATABASE_URL must use postgresql+asyncpg://... for SQLAlchemy async")

    return create_async_engine(url, pool_pre_ping=True)


_async_engine = _make_async_engine()
AsyncSessionLocal = async_sessionmaker(bind=_async_engine, autoflush=False, expire_on_commit=False)


@dataclass
class AsyncUnitOfWork(IAsyncUnitOfWork):
    """One entry point for DB work with an explicit async transaction boundary."""

    session: AsyncSession | None = None
    _committed: bool = False

    async def __aenter__(self) -> "AsyncUnitOfWork":
        if self.session is None:
            self.session = AsyncSessionLocal()

        self._committed = False

        # Wire repos to the same session
        self.table_users = UsersRepo(self.session)
        self.table_events = EventsRepo(self.session)
        self.table_venues = VenuesRepo(self.session)
        self.table_shows = ShowsRepo(self.session)
        self.table_pricing = PricingsRepo(self.session)
        self.table_inventory = InventoryRepo(self.session)
        self.table_bookings = BookingsRepo(self.session)
        self.table_payments = PaymentsRepo(self.session)
        self.table_tickets = TicketsRepo(self.session)
        self.table_read = ReadsRepo(self.session)

        return self

    async def commit(self) -> None:
        assert self.session is not None
        try:
            await self.session.commit()
            self._committed = True
        except IntegrityError as e:
            await self.session.rollback()
            raise RepositoryError(str(e)) from e

    async def rollback(self) -> None:
        assert self.session is not None
        await self.session.rollback()

    async def close(self) -> None:
        assert self.session is not None
        await self.session.close()

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        if self.session is None:
            return False

        # Always rollback on exception
        if exc_type is not None:
            await self.rollback()
        else:
            # If caller forgot to commit, rollback by default (safe)
            if not self._committed:
                await self.rollback()

        await self.close()
        return False


def uow_factory() -> AsyncUnitOfWork:
    """Convenience factory (nice for DI in FastAPI)."""
    return AsyncUnitOfWork()
