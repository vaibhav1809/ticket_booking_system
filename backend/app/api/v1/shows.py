from typing import List
from fastapi import APIRouter, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ...services.shows import IShowService, ShowListItem, ShowService

from ...config.auth import enable_auth, get_user
from ...config import log

router = APIRouter()


@router.get("")
@enable_auth
async def get_events(
    request: Request,
    category: str = Query(...),
    city: str = Query(...),
):
    log.info("[/show] api called")

    service: IShowService = ShowService()
    response_payload: List[ShowListItem] = await service.list_shows(
        category=category,
        city=city
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response_payload),
    )


@router.get("/{show_id}")
@enable_auth
async def book_a_seat(
    request: Request,
    show_id: str,
):

    log.info(f"[/show/{show_id}] api called")

    service: IShowService = ShowService()
    response_payload = await service.get_show(show_id=int(show_id))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response_payload),
    )
