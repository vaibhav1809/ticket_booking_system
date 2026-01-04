from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Inventory, InventoryStatus
from .interfaces import IInventoryRepo


class InventoryRepo(IInventoryRepo):
    """Repository for seat-level inventory operations.

    This repo is concurrency-critical.
    - `lock_for_update()` uses SELECT ... FOR UPDATE to lock inventory rows.
    - `set_status()` / `mark_booked()` perform bulk updates.

    All operations run within the caller's transaction boundary (UnitOfWork).
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def lock_for_update(self, *, show_id: int, seat_ids: Sequence[int]) -> list[Inventory]:
        """Lock inventory rows for the given seats in a show.

        Returns the locked Inventory ORM rows.
        """
        stmt = (
            select(Inventory)
            .where(Inventory.show_id == show_id, Inventory.seat_id.in_(list(seat_ids)))
            .with_for_update()
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def set_status(
        self,
        *,
        show_id: int,
        seat_ids: Sequence[int],
        status: InventoryStatus,
        booked_by: Optional[int] = None,
    ) -> int:
        """Bulk update inventory status for seats in a show.

        Returns the number of affected rows.
        """
        stmt = (
            update(Inventory)
            .where(Inventory.show_id == show_id, Inventory.seat_id.in_(list(seat_ids)))
            .values(status=status, booked_by=booked_by)
        )
        result = await self.session.execute(stmt)
        return int(result.rowcount or 0)                # type: ignore

    async def mark_booked(self, *, show_id: int, seat_ids: Sequence[int], booked_by: int) -> int:
        """Mark seats as booked for a show.

        Returns the number of affected rows.
        """
        return await self.set_status(
            show_id=show_id,
            seat_ids=seat_ids,
            status=InventoryStatus.available,
            booked_by=booked_by,
        )
