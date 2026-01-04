from typing import List
from pydantic import BaseModel


class SeatBookingRequest(BaseModel):
    show_id: str
    seat_ids: List[str]