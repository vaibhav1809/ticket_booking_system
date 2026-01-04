from fastapi import APIRouter

from ...config import log

router = APIRouter()


@router.get("")
async def get_payments():
    """Health check endpoint.

    Returns:
        dict: Health status information.
    """
    log.info("get_payments_called")
    return {"status": "healthy", "version": "1.0.0"}
