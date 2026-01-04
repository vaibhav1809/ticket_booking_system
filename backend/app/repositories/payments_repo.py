

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Payment, PaymentStatus
from .interfaces import IPaymentsRepo


class PaymentsRepo(IPaymentsRepo):
    """Repository for payment operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        booking_id: int,
        provider: Any,
        status: PaymentStatus,
        amount: int,
        currency: str,
        created_at: datetime,
    ) -> Payment:
        payment = Payment(
            booking_id=booking_id,
            provider=provider,
            status=status,
            amount=amount,
            currency=currency,
            created_at=created_at,
        )
        self.session.add(payment)
        await self.session.flush()  # populate payment_id
        return payment

    async def set_status(self, *, payment_id: int, status: PaymentStatus) -> None:
        stmt = update(Payment).where(Payment.payment_id == payment_id).values(status=status)
        await self.session.execute(stmt)
