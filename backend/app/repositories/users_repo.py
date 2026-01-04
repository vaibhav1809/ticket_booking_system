

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from .interfaces import IUsersRepo


class UsersRepo(IUsersRepo):
    """Repository for user operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email_id == email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create(
        self,
        *,
        email_id: str,
        phone: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        password_hash: Optional[bytes] = None,
    ) -> User:
        user = User(
            email_id=email_id,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            password_hash=password_hash,
        )
        self.session.add(user)
        await self.session.flush()  # populate user_id
        return user
