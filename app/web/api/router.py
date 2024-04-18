from fastapi.routing import APIRouter

from app.web.api import bookings

api_router = APIRouter()
api_router.include_router(
    router=bookings.router, 
    tags=["Bookings"],
)
