from ...api.v1.health import router as health_router
from ...api.v1.bookings import router as bookings_router
from ...api.v1.payments import router as payments_router

all_routes = [
    {'router': health_router, 'prefix': '/health', 'tags': ['health']},
    {'router': bookings_router, 'prefix': '/bookings', 'tags': ['bookings']},
    {'router': payments_router, 'prefix': '/payments', 'tags': ['payments']},
]
