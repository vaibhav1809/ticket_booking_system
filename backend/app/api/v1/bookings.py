from fastapi import APIRouter
from app.config import log

router = APIRouter()


@router.get("")
async def get_bookings():
    """Health check endpoint.

    Returns:
        dict: Health status information.
    """
    log.info("get_bookings_called")
    return {"status": "healthy", "version": "1.0.0"}
