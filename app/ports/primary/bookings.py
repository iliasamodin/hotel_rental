from abc import ABC, abstractmethod

from app.core.services.bookings.schemas import (
    BookingRequestSchema,
    BookingResponseSchema,
    ExtendedBookingResponseSchema,
    ExtendedHotelResponseSchema,
    ExtendedRoomResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ServiceVarietyResponseSchema,
)
from app.core.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator


class BookingServicePort(ABC):
    """
    Primary port of service for booking.
    """

    @abstractmethod
    async def get_services(
        self,
        only_for_hotels_and_only_for_rooms: HotelsOrRoomsValidator,
    ) -> list[ServiceVarietyResponseSchema]: ...

    @abstractmethod
    async def get_hotels(
        self,
        location: str | None = None,
        number_of_guests: int | None = None,
        stars: int | None = None,
        services: list[int] | None = None,
    ) -> list[ExtendedHotelResponseSchema]: ...

    @abstractmethod
    async def get_premium_levels(
        self,
        hotel_id: int | None = None,
        connected_with_rooms: bool = False,
    ) -> list[PremiumLevelVarietyResponseSchema]: ...

    @abstractmethod
    async def get_rooms(
        self,
        min_price_and_max_price: PriceRangeValidator,
        hotel_id: int = None,
        number_of_guests: int = None,
        services: list[int] | None = None,
        premium_levels: list[int] | None = None,
    ) -> list[ExtendedRoomResponseSchema]: ...

    @abstractmethod
    async def get_bookings(
        self,
        user_id: int,
        min_and_max_dts: MinAndMaxDtsValidator,
        number_of_guests: int = None,
    ) -> list[ExtendedBookingResponseSchema]: ...

    @abstractmethod
    async def add_booking(
        self,
        user_id: int,
        booking_data: BookingRequestSchema,
    ) -> BookingResponseSchema: ...

    @abstractmethod
    async def delete_booking(
        self,
        user_id: int,
        booking_id: int,
    ) -> BookingResponseSchema: ...
