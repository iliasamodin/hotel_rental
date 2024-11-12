from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import sessionmaker
from starlette import status

from app.settings import settings

from app.services.bookings.service import BookingService
from app.services.bookings.schemas import (
    BookingRequestSchema,
    BookingResponseSchema,
    ServiceVarietyResponseSchema,
    ExtendedHotelResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ExtendedBookingResponseSchema,
    ExtendedRoomResponseSchema,
)
from app.services.check.services import (
    get_min_and_max_dts,
    get_session_maker,
    get_only_for_hotels_and_only_for_rooms,
    get_min_price_and_max_price,
)
from app.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator

from app.web.api.dependencies import get_user_id
from app.web.api.bookings.types import hotel_stars_annotated, service_ids_annotated, premium_level_ids_annotated
from app.web.api.bookings.responses import (
    responses_of_getting_services,
    responses_of_getting_hotels,
    responses_of_getting_premium_levels,
    responses_of_getting_rooms,
    responses_of_getting_bookings,
    responses_of_adding_booking,
    responses_of_deleting_booking,
)

from app.redis.redis_controller import redis_controller

router = APIRouter(prefix="/bookings")


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=responses_of_getting_bookings,
    summary="Get a list of user's bookings.",
)
async def get_bookings(
    min_and_max_dts: MinAndMaxDtsValidator = Depends(get_min_and_max_dts),
    number_of_guests: int = None,
    user_id: int = Depends(get_user_id),
    session_maker: sessionmaker = Depends(get_session_maker),
) -> list[ExtendedBookingResponseSchema]:
    booking_service = BookingService(session_maker=session_maker)
    bookings: list[ExtendedBookingResponseSchema] = await booking_service.get_bookings(
        user_id=user_id,
        min_and_max_dts=min_and_max_dts,
        number_of_guests=number_of_guests,
    )

    return bookings


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=responses_of_adding_booking,
    summary="Add a booking.",
)
async def add_booking(
    booking_data: BookingRequestSchema,
    user_id: int = Depends(get_user_id),
    session_maker: sessionmaker = Depends(get_session_maker),
) -> BookingResponseSchema:
    booking_service = BookingService(session_maker=session_maker)
    booking: BookingResponseSchema = await booking_service.add_booking(
        user_id=user_id,
        booking_data=booking_data,
    )

    return booking


@router.delete(
    path="/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses_of_deleting_booking,
    summary="Delete booking.",
)
async def delete_booking(
    booking_id: int,
    user_id: int = Depends(get_user_id),
    session_maker: sessionmaker = Depends(get_session_maker),
) -> None:
    booking_service = BookingService(session_maker=session_maker)
    await booking_service.delete_booking(
        booking_id=booking_id,
        user_id=user_id,
    )


@router.get(
    path="/services",
    status_code=status.HTTP_200_OK,
    responses=responses_of_getting_services,
    summary="Get all service options.",
)
@redis_controller.cache(
    warming_up=True,
    expire=settings.CACHE_RETENTION_TIME_SECONDS,
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


@router.get(
    path="/hotels",
    status_code=status.HTTP_200_OK,
    responses=responses_of_getting_hotels,
    summary="Get a list of hotels in accordance with filters.",
)
@redis_controller.cache(
    warming_up=True,
    expire=settings.CACHE_RETENTION_TIME_SECONDS,
)
async def get_hotels(
    location: str = None,
    number_of_guests: int = None,
    stars: hotel_stars_annotated = None,  # type: ignore
    services: service_ids_annotated = None,  # type: ignore
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
    path="/premium-levels",
    status_code=status.HTTP_200_OK,
    responses=responses_of_getting_premium_levels,
    summary="Get all variations of room's premium levels.",
)
@redis_controller.cache(
    warming_up=True,
    expire=settings.CACHE_RETENTION_TIME_SECONDS,
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


@router.get(
    path="/rooms",
    status_code=status.HTTP_200_OK,
    responses=responses_of_getting_rooms,
    summary="Get a list of rooms in accordance with filters.",
)
@redis_controller.cache(
    warming_up=True,
    expire=settings.CACHE_RETENTION_TIME_SECONDS,
)
async def get_rooms(
    min_price_and_max_price: PriceRangeValidator = Depends(get_min_price_and_max_price),
    hotel_id: int = None,
    number_of_guests: int = None,
    services: service_ids_annotated = None,  # type: ignore
    premium_levels: premium_level_ids_annotated = None,  # type: ignore
    session_maker: sessionmaker = Depends(get_session_maker),
) -> list[ExtendedRoomResponseSchema]:
    booking_service = BookingService(session_maker=session_maker)
    rooms: list[ExtendedRoomResponseSchema] = await booking_service.get_rooms(
        min_price_and_max_price=min_price_and_max_price,
        hotel_id=hotel_id,
        number_of_guests=number_of_guests,
        services=services,
        premium_levels=premium_levels,
    )

    return rooms
