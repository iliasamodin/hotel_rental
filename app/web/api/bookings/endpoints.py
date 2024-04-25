from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import sessionmaker

from app.services.bookings.service import BookingService
from app.services.bookings.schemas import (
    ServiceVarietyResponseSchema,
    ListOfServicesRequestSchema,
    ExtendedHotelResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ServicesAndLevelsRequestSchema,
    ExtendedRoomResponseSchema,
)
from app.services.check.services import (
    get_session_maker,
    get_only_for_hotels_and_only_for_rooms,
    get_min_price_and_max_price,
)
from app.services.check.schemas import HotelsOrRoomsValidator, PriceRangeValidator

from app.web.api.bookings.types import hotel_stars_annotated

router = APIRouter(prefix="/bookings")


@router.get(
    path="/get-services",
    summary="Get all service options.",
)
async def get_services(
    only_for_hotels_and_only_for_rooms: HotelsOrRoomsValidator = Depends(get_only_for_hotels_and_only_for_rooms),
    session_maker: sessionmaker = Depends(get_session_maker),
) -> list[ServiceVarietyResponseSchema]:
    booking_service = BookingService(session_maker=session_maker)
    services: list[ServiceVarietyResponseSchema] = await booking_service.get_services(
        only_for_hotels_and_only_for_rooms=only_for_hotels_and_only_for_rooms
    )

    return services


@router.post(
    path="/get-hotels",
    summary="Get a list of hotels in accordance with filters.",
)
async def get_hotels(
    location: str = None,
    number_of_guests: int = None,
    stars: hotel_stars_annotated = None,
    services: ListOfServicesRequestSchema = None,
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


@router.get(
    path="/get-premium-levels",
    summary="Get all variations of room's premium levels.",
)
async def get_premium_levels(
    hotel_id: int = None,
    connected_with_rooms: bool = False,
    session_maker: sessionmaker = Depends(get_session_maker),
) -> list[PremiumLevelVarietyResponseSchema]:
    booking_service = BookingService(session_maker=session_maker)
    premium_levels: list[PremiumLevelVarietyResponseSchema] = await booking_service.get_premium_levels(
        hotel_id=hotel_id,
        connected_with_rooms=connected_with_rooms,
    )

    return premium_levels


@router.post(
    path="/get-rooms",
    summary="Get a list of rooms in accordance with filters.",
)
async def get_rooms(
    min_price_and_max_price: PriceRangeValidator = Depends(get_min_price_and_max_price),
    hotel_id: int = None,
    number_of_guests: int = None,
    services_and_levels: ServicesAndLevelsRequestSchema = None,
    session_maker: sessionmaker = Depends(get_session_maker),
) -> list[ExtendedRoomResponseSchema]:
    booking_service = BookingService(session_maker=session_maker)
    rooms: list[ExtendedRoomResponseSchema] = await booking_service.get_rooms(
        min_price_and_max_price=min_price_and_max_price,
        hotel_id=hotel_id,
        number_of_guests=number_of_guests,
        services_and_levels=services_and_levels,
    )

    return rooms
