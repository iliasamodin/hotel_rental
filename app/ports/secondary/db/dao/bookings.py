from abc import ABC, abstractmethod

from app.ports.secondary.db.dao.base import BaseDAOPort

from app.core.services.bookings.dtos import (
    ExtendedBookingDTO,
    ExtendedHotelDTO,
    ExtendedRoomDTO,
    PremiumLevelVarietyDTO,
    ServiceVarietyDTO,
)
from app.core.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator


class BookingDAOPort(BaseDAOPort, ABC):
    """
    Secondary port of DAO for booking.
    """

    @abstractmethod
    async def get_services(
        self,
        only_for_hotels_and_only_for_rooms: HotelsOrRoomsValidator,
    ) -> list[ServiceVarietyDTO]: ...

    @abstractmethod
    async def get_hotels(
        self,
        location: str | None = None,
        number_of_guests: int | None = None,
        stars: int | None = None,
        services: list[int] | None = None,
    ) -> list[ExtendedHotelDTO]: ...

    @abstractmethod
    async def get_premium_levels(
        self,
        hotel_id: int | None = None,
        connected_with_rooms: bool = False,
    ) -> list[PremiumLevelVarietyDTO]: ...

    @abstractmethod
    async def get_rooms(
        self,
        min_price_and_max_price: PriceRangeValidator,
        hotel_id: int = None,
        number_of_guests: int = None,
        services: list[int] | None = None,
        premium_levels: list[int] | None = None,
    ) -> list[ExtendedRoomDTO]: ...

    @abstractmethod
    async def get_bookings(
        self,
        min_and_max_dts: MinAndMaxDtsValidator,
        number_of_guests: int = None,
        user_id: int | None = None,
        room_id: int | None = None,
        booking_overlaps: bool = False,
    ) -> list[ExtendedBookingDTO]: ...
