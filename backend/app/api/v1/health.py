from fastapi import APIRouter

from ...config import log

router = APIRouter()


@router.get("")
async def health_check():
    """Health check endpoint.

    Returns:
        dict: Health status information.
    """
    log.info("health_check_called")
    return {"status": "healthy", "version": "1.0.0"}
