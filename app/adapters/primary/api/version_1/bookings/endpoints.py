from fastapi import Depends
from fastapi.routing import APIRouter
from starlette import status

from app.settings import settings

from app.ports.primary.bookings import BookingServicePort

from app.core.services.bookings.schemas import (
    BookingRequestSchema,
    BookingResponseSchema,
    ServiceVarietyResponseSchema,
    ExtendedHotelResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ExtendedBookingResponseSchema,
    ExtendedRoomResponseSchema,
)
from app.dependencies.check import (
    get_min_and_max_dts,
    get_only_for_hotels_and_only_for_rooms,
    get_min_price_and_max_price,
)
from app.core.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator

from app.dependencies.auth import get_user_id
from app.adapters.primary.api.version_1.bookings.types import (
    hotel_stars_annotated,
    service_ids_annotated,
    premium_level_ids_annotated,
)
from app.adapters.primary.api.version_1.bookings.responses import (
    responses_of_getting_services,
    responses_of_getting_hotels,
    responses_of_getting_premium_levels,
    responses_of_getting_rooms,
    responses_of_getting_bookings,
    responses_of_adding_booking,
    responses_of_deleting_booking,
)

from app.utils.redis.redis_controller import redis_controller

from app.dependencies.bookings import get_booking_service

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
    service: BookingServicePort = Depends(get_booking_service),
) -> list[ExtendedBookingResponseSchema]:
    bookings: list[ExtendedBookingResponseSchema] = await service.get_bookings(
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
    service: BookingServicePort = Depends(get_booking_service),
) -> BookingResponseSchema:
    booking: BookingResponseSchema = await service.add_booking(
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
    service: BookingServicePort = Depends(get_booking_service),
) -> None:
    await service.delete_booking(
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
    service: BookingServicePort = Depends(get_booking_service),
) -> list[ServiceVarietyResponseSchema]:
    services: list[ServiceVarietyResponseSchema] = await service.get_services(
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
    service: BookingServicePort = Depends(get_booking_service),
) -> list[ExtendedHotelResponseSchema]:
    hotels: list[ExtendedHotelResponseSchema] = await service.get_hotels(
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
    service: BookingServicePort = Depends(get_booking_service),
) -> list[PremiumLevelVarietyResponseSchema]:
    premium_levels: list[PremiumLevelVarietyResponseSchema] = await service.get_premium_levels(
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
    service: BookingServicePort = Depends(get_booking_service),
) -> list[ExtendedRoomResponseSchema]:
    rooms: list[ExtendedRoomResponseSchema] = await service.get_rooms(
        min_price_and_max_price=min_price_and_max_price,
        hotel_id=hotel_id,
        number_of_guests=number_of_guests,
        services=services,
        premium_levels=premium_levels,
    )

    return rooms
