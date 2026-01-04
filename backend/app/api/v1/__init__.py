from .health import router as health_router
from .book import router as book_router
from .shows import router as shows_router

all_routes = [
    {'router': health_router, 'prefix': '/health', 'tags': ['health']},
    {'router': book_router, 'prefix': '/book', 'tags': ['book']},
    {'router': shows_router, 'prefix': '/show', 'tags': ['show']},
]
