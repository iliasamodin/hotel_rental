from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import sessionmaker

from app.services.bookings.service import BookingService
from app.services.bookings.schemas import (
    ServiceVarietyResponseSchema,
    ListOfServicesRequestSchema,
    ExtendedHotelResponseSchema,
)
from app.services.check.services import get_session_maker, get_only_for_hotels_and_only_for_rooms
from app.services.check.schemas import HotelsOrRoomsValidator

from app.web.api.bookings.types import hotel_stars_annotated

router = APIRouter(prefix="/bookings")


@router.get(
    path="/get-services",
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


@router.post(
    path="/get-hotels",
    summary="Get a list of hotels in accordance with filters.",
)
async def get_hotels(
    location: str | None = None,
    number_of_guests: int | None = None,
    stars: hotel_stars_annotated = None,
    services: ListOfServicesRequestSchema | None = None,
    session_maker: sessionmaker = Depends(get_session_maker),
) -> list[ExtendedHotelResponseSchema]:
    booking_service = BookingService(session_maker=session_maker)
    hotels: list[ExtendedHotelResponseSchema] = await booking_service.get_hotels(
        location=location,
        number_of_guests=number_of_guests,
        stars=stars,
        services=services,
    )

    return hotels
