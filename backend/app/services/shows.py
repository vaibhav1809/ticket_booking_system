
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Protocol, runtime_checkable

from sqlalchemy import func, select

from ..db.models import Event, Show, ShowPricing, Venue
from ..repositories.uow import AsyncUnitOfWork



@dataclass(frozen=True)
class ShowListItem:
    """Response DTO for the show listing cards."""

    show_id: int
    event_id: int
    category: str  # "movie" | "concert" (matches events.event_type)
    title: str
    start_time: datetime
    end_time: datetime
    venue_name: str
    city: str
    min_price: int
    currency: str


# ShowDetails DTO for full show details
@dataclass(frozen=True)
class ShowDetails:
    """Full details for a show (Show + Event + Venue)."""

    # Show
    show_id: int
    start_time: datetime
    end_time: datetime
    status: str

    # Event
    event_id: int
    category: str  # events.event_type
    title: str
    duration_min: int
    language: str
    genre: str

    # Venue
    venue_id: int
    venue_name: str
    location: str
    city: str
    country: str
    pincode: str
    address: str


@runtime_checkable
class IShowService(Protocol):
    async def get_show(self, show_id: int) -> ShowDetails | None: ...

    async def list_shows(self, category: str, city: str) -> List[ShowListItem]: ...

    async def create_show(self, show_data: dict): ...

    async def update_show(self, show_id: int, show_data: dict): ...

    async def delete_show(self, show_id: int): ...


class ShowService(IShowService):
    async def get_show(self, show_id: int) -> ShowDetails | None:
        """Fetch a show with its Event + Venue details.

        Returns:
            ShowDetails if the show exists, else None.
        """

        if show_id <= 0:
            raise ValueError("show_id must be a positive integer")

        stmt = (
            select(
                # Show
                Show.show_id.label("show_id"),
                Show.start_time.label("start_time"),
                Show.end_time.label("end_time"),
                Show.status.label("status"),
                # Event
                Event.event_id.label("event_id"),
                Event.event_type.label("category"),
                Event.title.label("title"),
                Event.duration_min.label("duration_min"),
                Event.language.label("language"),
                Event.genre.label("genre"),
                # Venue
                Venue.venue_id.label("venue_id"),
                Venue.name.label("venue_name"),
                Venue.location.label("location"),
                Venue.city.label("city"),
                Venue.country.label("country"),
                Venue.pincode.label("pincode"),
                Venue.address.label("address"),
            )
            .select_from(Show)
            .join(Event, Event.event_id == Show.event_id)
            .join(Venue, Venue.venue_id == Show.venue_id)
            .where(Show.show_id == show_id)
        )

        async with AsyncUnitOfWork() as uow:
            row = (await uow.session.execute(stmt)).mappings().first()  # type: ignore[attr-defined]

        if row is None:
            return None

        return ShowDetails(
            # Show
            show_id=int(row["show_id"]),
            start_time=row["start_time"],
            end_time=row["end_time"],
            status=str(row["status"]),
            # Event
            event_id=int(row["event_id"]),
            category=str(row["category"]),
            title=str(row["title"]),
            duration_min=int(row["duration_min"]),
            language=str(row["language"]),
            genre=str(row["genre"]),
            # Venue
            venue_id=int(row["venue_id"]),
            venue_name=str(row["venue_name"]),
            location=str(row["location"]),
            city=str(row["city"]),
            country=str(row["country"]),
            pincode=str(row["pincode"]),
            address=str(row["address"]),
        )

    async def list_shows(self, category: str, city: str) -> List[ShowListItem]:
        """List shows for UI cards.

        Args:
            category: "movie" | "concert" | "all"
            city: "Bangalore" | "Mumbai" (case-insensitive)

        Returns:
            List of ShowListItem ordered by start_time.

        Notes:
            - Uses UNION ALL for category == "all" to keep the intent explicit.
            - Computes min price per show from show_pricings.
        """

        category_norm = (category or "").strip().lower()
        city_norm = (city or "").strip().lower()

        if category_norm not in {"movie", "concert", "all"}:
            raise ValueError("category must be one of: movie, concert, all")

        if city_norm not in {"bangalore", "mumbai"}:
            raise ValueError("city must be either Bangalore or Mumbai")

        def _base_stmt(event_type: str):
            return (
                select(
                    Show.show_id.label("show_id"),
                    Event.event_id.label("event_id"),
                    Event.event_type.label("category"),
                    Event.title.label("title"),
                    Show.start_time.label("start_time"),
                    Show.end_time.label("end_time"),
                    Venue.name.label("venue_name"),
                    Venue.city.label("city"),
                    func.min(ShowPricing.amount).label("min_price"),
                    func.min(ShowPricing.currency).label("currency"),
                )
                .select_from(Show)
                .join(Event, Event.event_id == Show.event_id)
                .join(Venue, Venue.venue_id == Show.venue_id)
                .join(ShowPricing, ShowPricing.show_id == Show.show_id)
                .where(func.lower(Venue.city) == city_norm)
                .where(Event.event_type == event_type)
                .group_by(
                    Show.show_id,
                    Event.event_id,
                    Event.event_type,
                    Event.title,
                    Show.start_time,
                    Show.end_time,
                    Venue.name,
                    Venue.city,
                )
            )

        async with AsyncUnitOfWork() as uow:
            if category_norm == "all":
                movies = _base_stmt("movie")
                concerts = _base_stmt("concert")
                stmt = movies.union_all(concerts).order_by("start_time")
            else:
                stmt = _base_stmt(category_norm).order_by("start_time")

            rows = (await uow.session.execute(stmt)).mappings().all()  # type: ignore[attr-defined]

        # Map rows -> DTOs
        out: List[ShowListItem] = []
        for r in rows:
            out.append(
                ShowListItem(
                    show_id=int(r["show_id"]),
                    event_id=int(r["event_id"]),
                    category=str(r["category"]),
                    title=str(r["title"]),
                    start_time=r["start_time"],
                    end_time=r["end_time"],
                    venue_name=str(r["venue_name"]),
                    city=str(r["city"]),
                    min_price=int(r["min_price"]),
                    currency=str(r["currency"]),
                )
            )

        return out

    async def create_show(self, show_data: dict):
        # Not implemented in this step
        raise NotImplementedError

    async def update_show(self, show_id: int, show_data: dict):
        # Not implemented in this step
        raise NotImplementedError

    async def delete_show(self, show_id: int):
        # Not implemented in this step
        raise NotImplementedError
