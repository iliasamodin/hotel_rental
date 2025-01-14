from fastapi.routing import APIRouter

from app.api.version_1 import authorization
from app.api.version_1 import resource_manager
from app.api.version_1 import bookings

api_router = APIRouter(prefix="/v1")
api_router.include_router(
    router=authorization.router,
    tags=["Authorization"],
)
api_router.include_router(
    router=resource_manager.router,
    tags=["Resource Manager"],
)
api_router.include_router(
    router=bookings.router,
    tags=["Bookings"],
)
