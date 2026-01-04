"""SQLAlchemy ORM models for the ticket booking system."""

from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# -------------------------
# Enums (Postgres ENUMs)
# -------------------------


class EventType(str, enum.Enum):
    movie = "movie"
    concert = "concert"
    theatre = "theatre"
    sport = "sport"


class ShowStatus(str, enum.Enum):
    draft = "draft"
    live = "live"
    sold_out = "sold_out"
    cancelled = "cancelled"


class InventoryStatus(str, enum.Enum):
    available = "available"
    not_available = "not_available"


class BookingStatus(str, enum.Enum):
    initiated = "initiated"
    confirmed = "confirmed"
    cancelled = "cancelled"
    expired = "expired"


class TicketStatus(str, enum.Enum):
    active = "active"
    cancelled = "cancelled"
    used = "used"


class PaymentProvider(str, enum.Enum):
    upi = "upi"
    credit_card = "credit-card"
    debit_card = "debit-card"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


# -------------------------
# Tables
# -------------------------


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    password_hash: Mapped[Optional[bytes]] = mapped_column(BYTEA, nullable=True)

    # Relationships
    created_events: Mapped[List[Event]] = relationship(
        back_populates="creator",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    bookings: Mapped[List[Booking]] = relationship(back_populates="user")
    inventories_booked: Mapped[List[Inventory]] = relationship(
        back_populates="booked_by_user",
        foreign_keys="Inventory.booked_by",
    )


class Event(Base):
    __tablename__ = "events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[EventType] = mapped_column(
        SAEnum(EventType, name="event_type", native_enum=True),
        nullable=False,
    )
    duration_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    language: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    genre: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
    )
    last_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)

    # Relationships
    creator: Mapped[Optional[User]] = relationship(back_populates="created_events")
    shows: Mapped[List[Show]] = relationship(back_populates="event", cascade="all, delete-orphan")


class Venue(Base):
    __tablename__ = "venues"

    venue_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    pincode: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    sections: Mapped[List[VenueSection]] = relationship(
        back_populates="venue",
        cascade="all, delete-orphan",
    )
    shows: Mapped[List[Show]] = relationship(back_populates="venue")


class VenueSection(Base):
    __tablename__ = "venue_sections"

    section_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venue_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("venues.venue_id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    venue: Mapped[Venue] = relationship(back_populates="sections")
    seats: Mapped[List[VenueSeat]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
    )
    show_pricings: Mapped[List[ShowPricing]] = relationship(back_populates="section")

    __table_args__ = (
        UniqueConstraint("venue_id", "name", name="uq_venue_sections_venue_id_name"),
    )


class VenueSeat(Base):
    __tablename__ = "venue_seats"

    seat_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("venue_sections.section_id", ondelete="CASCADE"),
        nullable=False,
    )
    row_nums: Mapped[int] = mapped_column(Integer, nullable=False)
    col_nums: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    section: Mapped[VenueSection] = relationship(back_populates="seats")
    inventories: Mapped[List[Inventory]] = relationship(back_populates="seat")
    tickets: Mapped[List[Ticket]] = relationship(back_populates="seat")

    __table_args__ = (
        UniqueConstraint(
            "section_id",
            "row_nums",
            "col_nums",
            name="uq_venue_seats_section_row_col"),
    )


class Show(Base):
    __tablename__ = "shows"

    show_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("events.event_id", ondelete="CASCADE"),
        nullable=False,
    )
    venue_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("venues.venue_id", ondelete="CASCADE"),
        nullable=False,
    )
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[ShowStatus] = mapped_column(
        SAEnum(ShowStatus, name="show_type", native_enum=True),
        nullable=False,
        default=ShowStatus.draft,
    )

    # Relationships
    event: Mapped[Event] = relationship(back_populates="shows")
    venue: Mapped[Venue] = relationship(back_populates="shows")
    pricings: Mapped[List[ShowPricing]] = relationship(
        back_populates="show",
        cascade="all, delete-orphan",
    )
    inventories: Mapped[List[Inventory]] = relationship(
        back_populates="show",
        cascade="all, delete-orphan",
    )
    bookings: Mapped[List[Booking]] = relationship(back_populates="show")
    tickets: Mapped[List[Ticket]] = relationship(back_populates="show")


class ShowPricing(Base):
    __tablename__ = "show_pricings"

    show_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("shows.show_id", ondelete="CASCADE"),
        nullable=False,
    )
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("venue_sections.section_id", ondelete="CASCADE"),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    # Relationships
    show: Mapped[Show] = relationship(back_populates="pricings")
    section: Mapped[VenueSection] = relationship(back_populates="show_pricings")

    __table_args__ = (
        PrimaryKeyConstraint("show_id", "section_id", name="pk_show_pricings"),
    )


class Inventory(Base):
    __tablename__ = "inventories"

    show_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("shows.show_id", ondelete="CASCADE"),
        nullable=False,
    )
    seat_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("venue_seats.seat_id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[InventoryStatus] = mapped_column(
        SAEnum(InventoryStatus, name="inventory_status", native_enum=True),
        nullable=False,
        default=InventoryStatus.available,
    )
    booked_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
    )
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    # Relationships
    show: Mapped[Show] = relationship(back_populates="inventories")
    seat: Mapped[VenueSeat] = relationship(back_populates="inventories")
    booked_by_user: Mapped[Optional[User]] = relationship(
        back_populates="inventories_booked",
        foreign_keys=[booked_by],
    )

    __table_args__ = (
        PrimaryKeyConstraint("show_id", "seat_id", name="pk_inventories"),
    )


class Booking(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    show_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("shows.show_id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[BookingStatus] = mapped_column(
        SAEnum(BookingStatus, name="booking_status", native_enum=True),
        nullable=False,
        default=BookingStatus.initiated,
    )
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped[User] = relationship(back_populates="bookings")
    show: Mapped[Show] = relationship(back_populates="bookings")
    payments: Mapped[List[Payment]] = relationship(
        back_populates="booking",
        cascade="all, delete-orphan",
    )
    tickets: Mapped[List[Ticket]] = relationship(back_populates="booking")


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("bookings.booking_id", ondelete="CASCADE"),
        nullable=False,
    )
    provider: Mapped[PaymentProvider] = mapped_column(
        SAEnum(PaymentProvider, name="payment_provider", native_enum=True),
        nullable=False,
    )
    status: Mapped[PaymentStatus] = mapped_column(
        SAEnum(PaymentStatus, name="payment_status", native_enum=True),
        nullable=False,
        default=PaymentStatus.pending,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    booking: Mapped[Booking] = relationship(back_populates="payments")


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("bookings.booking_id", ondelete="CASCADE"),
        nullable=False,
    )
    seat_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("venue_seats.seat_id", ondelete="CASCADE"),
        nullable=False,
    )
    show_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("shows.show_id", ondelete="CASCADE"),
        nullable=False,
    )
    ticket_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    qr_payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    status: Mapped[TicketStatus] = mapped_column(
        SAEnum(TicketStatus, name="ticket_status", native_enum=True),
        nullable=False,
        default=TicketStatus.active,
    )
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    booking: Mapped[Booking] = relationship(back_populates="tickets")
    seat: Mapped[VenueSeat] = relationship(back_populates="tickets")
    show: Mapped[Show] = relationship(back_populates="tickets")
