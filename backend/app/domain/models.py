from pydantic import BaseModel
from .errors import InventoryStatus, BookingStatus, PaymentStatus
from typing import List, Optional
from datetime import datetime


class SeatRef(BaseModel):
    seat_id: int


class HoldSeatsRequest(BaseModel):
    user_id: int
    show_id: int
    seat_ids: List[int]


class HoldSeatsResponse(BaseModel):
    show_id: int
    seat_ids: List[int]
    hold_token: str
    hold_expires_at: datetime


class CreateBookingRequest(BaseModel):
    user_id: int
    show_id: int
    seat_ids: List[int]
    hold_token: str


class CreateBookingResponse(BaseModel):
    booking_id: int
    status: BookingStatus
    total_price_cents: int
    currency: str


class PaymentInitResponse(BaseModel):
    payment_id: int
    status: PaymentStatus
    provider_redirect_url: Optional[str] = None


class TicketDTO(BaseModel):
    ticket_id: int
    show_id: int
    seat_id: int
    ticket_code: str
    issued_at: datetime


class BookingDetailsResponse(BaseModel):
    booking_id: int
    status: BookingStatus
    tickets: List[TicketDTO]
