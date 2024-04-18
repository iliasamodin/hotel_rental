from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import sessionmaker

from app.services.bookings.service import BookingService
from app.services.bookings.schemas import ServiceVarietyResponseSchema
from app.services.check.services import get_session_maker, get_only_for_hotels_and_only_for_rooms
from app.services.check.schemas import HotelsOrRoomsValidator

router = APIRouter(prefix="/bookings")


@router.get(
    path="/services",
    summary="Get all service options.",
)
async def get_services(
    boolean_constraints_for_filters: HotelsOrRoomsValidator = Depends(get_only_for_hotels_and_only_for_rooms),
    session_maker: sessionmaker = Depends(get_session_maker),
) -> list[ServiceVarietyResponseSchema]:
    booking_service = BookingService(session_maker=session_maker)
    services: list[ServiceVarietyResponseSchema] = await booking_service.get_services(
        boolean_constraints_for_filters=boolean_constraints_for_filters
    )

    return services
