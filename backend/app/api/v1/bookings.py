import asyncio
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from .schema.request import SeatBookingRequest
from ...config.auth import enable_auth, get_user
from ...config import log
from ...services.bookings import IBookingService, BookingService

router = APIRouter()


@router.put("/reserve")
@enable_auth
async def reserve_seats(
    request: Request,
    payload: SeatBookingRequest,
):
    log.info("[/booking/reserve] api called")

    service: IBookingService = BookingService()
    asyncio.create_task(
        service.reserve_seats(show_id=str(payload.show_id), seat_ids=payload.seat_ids))

    response_payload = {
        "status": "accepted", **payload.model_dump()
    }
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=response_payload)


@router.put("/book")
@enable_auth
async def book_a_seat(
    request: Request,
    payload: SeatBookingRequest,
):
    # should fail after 1 min of try

    log.info("[/booking/book] api called")

    user_name = get_user(request)
    service: IBookingService = BookingService()
    await service.book_seats(user_id=user_name, show_id=str(payload.show_id), seat_ids=payload.seat_ids)

    response_payload = {
        "status": "seats_booked", **payload.model_dump()
    }

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_payload)
