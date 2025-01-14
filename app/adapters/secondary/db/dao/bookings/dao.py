from typing import Coroutine

from sqlalchemy.engine import Result

from app.ports.secondary.db.dao.bookings import BookingDAOPort

from app.adapters.secondary.db.dao.base.dao import BaseDAO
from app.adapters.secondary.db.dao.bookings.queries import (
    get_bookings,
    get_services,
    get_hotels,
    get_premium_levels,
    get_rooms,
)
from app.adapters.secondary.db.dao.bookings.helpers import get_filters_for_booking_overlaps, get_filters_for_bookings

from app.core.services.bookings.dtos import (
    ExtendedBookingDTO,
    ImageDTO,
    RoomDTO,
    ServiceVarietyDTO,
    ExtendedHotelDTO,
    PremiumLevelVarietyDTO,
    ExtendedRoomDTO,
    HotelDTO,
)
from app.core.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator


class BookingDAO(BaseDAO, BookingDAOPort):
    """
    DAO for booking.
    """

    async def get_services(
        self,
        only_for_hotels_and_only_for_rooms: HotelsOrRoomsValidator,
    ) -> list[ServiceVarietyDTO]:
        """
        Get all service options.

        :return: list of services.
        """

        query_result_of_services: Result | Coroutine = get_services(
            session=self.session,
            only_for_hotels_and_only_for_rooms=only_for_hotels_and_only_for_rooms,
        )
        if isinstance(query_result_of_services, Coroutine):
            query_result_of_services = await query_result_of_services

        rows_with_services = query_result_of_services.fetchall()

        services = [ServiceVarietyDTO.model_validate(row.ServiceVarietiesModel) for row in rows_with_services]

        return services

    async def get_hotels(
        self,
        location: str | None = None,
        number_of_guests: int | None = None,
        stars: int | None = None,
        services: list[int] | None = None,
    ) -> list[ExtendedHotelDTO]:
        """
        Get a list of hotels in accordance with filters.

        :return: list of hotels.
        """

        query_result_of_hotels: Result | Coroutine = get_hotels(
            session=self.session,
            location=location,
            number_of_guests=number_of_guests,
            stars=stars,
            services=services,
        )
        if isinstance(query_result_of_hotels, Coroutine):
            query_result_of_hotels = await query_result_of_hotels

        rows_with_hotels = query_result_of_hotels.fetchall()

        map_of_hotel_ids_and_hotels: dict[int, ExtendedHotelDTO] = {}
        for row in rows_with_hotels:
            hotel = ExtendedHotelDTO.model_validate(row.HotelsModel)
            hotel.rooms_quantity = row.rooms_quantity
            if row.ImagesModel is not None:
                hotel.main_image = ImageDTO.model_validate(row.ImagesModel)

            hotel.services = []
            if row.ServiceVarietiesModel is not None:
                hotel.services.append(ServiceVarietyDTO.model_validate(row.ServiceVarietiesModel))

            if hotel.id not in map_of_hotel_ids_and_hotels:
                map_of_hotel_ids_and_hotels[hotel.id] = hotel
            else:
                map_of_hotel_ids_and_hotels[hotel.id].services.extend(hotel.services)

        return map_of_hotel_ids_and_hotels.values()

    async def get_premium_levels(
        self,
        hotel_id: int | None = None,
        connected_with_rooms: bool = False,
    ) -> list[PremiumLevelVarietyDTO]:
        """
        Get all variations of room's premium levels.

        :return: list of premium levels.
        """

        query_result_of_premium_levels: Result | Coroutine = get_premium_levels(
            session=self.session,
            hotel_id=hotel_id,
            connected_with_rooms=connected_with_rooms,
        )
        if isinstance(query_result_of_premium_levels, Coroutine):
            query_result_of_premium_levels = await query_result_of_premium_levels

        rows_with_premium_levels = query_result_of_premium_levels.fetchall()

        premium_levels = [
            PremiumLevelVarietyDTO.model_validate(row.PremiumLevelVarietiesModel) for row in rows_with_premium_levels
        ]

        return premium_levels

    async def get_rooms(
        self,
        min_price_and_max_price: PriceRangeValidator,
        hotel_id: int = None,
        number_of_guests: int = None,
        services: list[int] | None = None,
        premium_levels: list[int] | None = None,
    ) -> list[ExtendedRoomDTO]:
        """
        Get a list of rooms in accordance with filters.

        :return: list of rooms.
        """

        query_result_of_rooms: Result | Coroutine = get_rooms(
            session=self.session,
            min_price_and_max_price=min_price_and_max_price,
            hotel_id=hotel_id,
            number_of_guests=number_of_guests,
            services=services,
            premium_levels=premium_levels,
        )
        if isinstance(query_result_of_rooms, Coroutine):
            query_result_of_rooms = await query_result_of_rooms

        rows_with_rooms = query_result_of_rooms.fetchall()

        map_of_room_ids_and_rooms: dict[int, ExtendedRoomDTO] = {}
        for row in rows_with_rooms:
            room = ExtendedRoomDTO.model_validate(row.RoomsModel)
            room.hotel = HotelDTO.model_validate(row.HotelsModel)
            room.premium_level = row.PremiumLevelVarietiesModel and PremiumLevelVarietyDTO.model_validate(
                row.PremiumLevelVarietiesModel,
            )

            room.services = []
            if row.ServiceVarietiesModel is not None:
                room.services.append(ServiceVarietyDTO.model_validate(row.ServiceVarietiesModel))

            if room.id not in map_of_room_ids_and_rooms:
                map_of_room_ids_and_rooms[room.id] = room
            else:
                map_of_room_ids_and_rooms[room.id].services.extend(room.services)

        return map_of_room_ids_and_rooms.values()

    async def get_bookings(
        self,
        min_and_max_dts: MinAndMaxDtsValidator,
        number_of_guests: int = None,
        user_id: int | None = None,
        room_id: int | None = None,
        booking_overlaps: bool = False,
    ) -> list[ExtendedBookingDTO]:
        """
        Get a list of user's bookings.

        :return: list of bookings.
        """

        query_result_of_bookings: Result | Coroutine = get_bookings(
            session=self.session,
            user_id=user_id,
            min_and_max_dts=min_and_max_dts,
            number_of_guests=number_of_guests,
            room_id=room_id,
            get_query_filters=get_filters_for_booking_overlaps if booking_overlaps else get_filters_for_bookings,
        )
        if isinstance(query_result_of_bookings, Coroutine):
            query_result_of_bookings = await query_result_of_bookings

        rows_with_bookings = query_result_of_bookings.fetchall()

        bookings: list[ExtendedBookingDTO] = []
        for row in rows_with_bookings:
            booking = ExtendedBookingDTO.model_validate(row.BookingsModel)
            booking.room = RoomDTO.model_validate(row.RoomsModel)
            bookings.append(booking)

        return bookings
