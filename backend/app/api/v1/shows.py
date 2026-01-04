from fastapi import APIRouter, Form, Request, status
from fastapi.responses import JSONResponse

from ...config.auth import enable_auth, get_user
from ...config import log

router = APIRouter()


@router.get("")
@enable_auth
async def get_events(
    request: Request,
    type: str = Form(...),
    city: str = Form(...),
):
    log.info("[/show] api called")

    

    response_payload = {
        "status": "accepted"
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_payload)


@router.get("/{show_id}")
async def book_a_seat(
    request: Request,
    show_id: str,
):

    log.info(f"[/show/{show_id}] api called")

    response_payload = {
        "status": "seats_booked"
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_payload)
