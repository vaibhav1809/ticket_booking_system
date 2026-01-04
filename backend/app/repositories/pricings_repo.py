

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import ShowPricing
from .interfaces import IPricingsRepo


class PricingsRepo(IPricingsRepo):
    """Repository for show pricing operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_for_show(self, show_id: int) -> list[ShowPricing]:
        stmt = select(ShowPricing).where(ShowPricing.show_id == show_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_price(self, *, show_id: int, section_id: int) -> ShowPricing | None:
        stmt = select(ShowPricing).where(
            ShowPricing.show_id == show_id,
            ShowPricing.section_id == section_id,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def upsert(
            self,
            *,
            show_id: int,
            section_id: int,
            amount: int,
            currency: str) -> ShowPricing:
        """Insert or update pricing for a (show_id, section_id) pair.

        Note: This assumes you have a UNIQUE constraint on (show_id, section_id).
        """

        # Preferred: Postgres ON CONFLICT upsert
        try:
            from sqlalchemy.dialects.postgresql import insert

            stmt = insert(ShowPricing).values(
                show_id=show_id,
                section_id=section_id,
                amount=amount,
                currency=currency,
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=[ShowPricing.show_id, ShowPricing.section_id],
                set_={"amount": amount, "currency": currency},
            ).returning(ShowPricing)

            res = await self.session.execute(stmt)
            row = res.scalar_one()
            await self.session.flush()
            return row
        except Exception:
            # Fallback: select then update/insert
            existing = await self.get_price(show_id=show_id, section_id=section_id)
            if existing:
                existing.amount = amount
                existing.currency = currency
                await self.session.flush()
                return existing

            created = ShowPricing(
                show_id=show_id,
                section_id=section_id,
                amount=amount,
                currency=currency,
            )
            self.session.add(created)
            await self.session.flush()
            return created
