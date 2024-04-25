from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.bookings.adapters import get_services, get_hotels, get_premium_levels, get_rooms
from app.dao.bookings.schemas import (
    ServiceVarietyDTO,
    ExtendedHotelDTO,
    PremiumLevelVarietyDTO,
    ExtendedRoomDTO,
    HotelDTO,
)

from app.services.check.schemas import HotelsOrRoomsValidator, PriceRangeValidator
from app.services.bookings.schemas import ListOfServicesRequestSchema, ServicesAndLevelsRequestSchema


class BookingDAO:
    """
    DAO for booking.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_services(
        self,
        only_for_hotels_and_only_for_rooms: HotelsOrRoomsValidator,
    ) -> list[ServiceVarietyDTO]:
        """
        Get all service options.

        :return: list of services.
        """

        query_result_of_services: Result = await get_services(
            session=self.session,
            only_for_hotels_and_only_for_rooms=only_for_hotels_and_only_for_rooms,
        )
        rows_with_services = query_result_of_services.fetchall()

        services = [
            ServiceVarietyDTO.model_validate(row.ServiceVarietiesModel)
            for row in rows_with_services
        ]

        return services

    async def get_hotels(
        self,
        location: str | None = None,
        number_of_guests: int | None = None,
        stars: int | None = None,
        services: ListOfServicesRequestSchema | None = None,
    ) -> list[ExtendedHotelDTO]:
        """
        Get a list of hotels in accordance with filters.

        :return: list of hotels.
        """

        query_result_of_hotels: Result = await get_hotels(
            session=self.session,
            location=location,
            number_of_guests=number_of_guests,
            stars=stars,
            services=services,
        )
        rows_with_hotels = query_result_of_hotels.fetchall()

        map_of_hotel_ids_and_hotels: dict[int, ExtendedHotelDTO] = {}
        for row in rows_with_hotels:
            hotel = ExtendedHotelDTO.model_validate(row.HotelsModel)
            hotel.rooms_quantity = row.rooms_quantity

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

        query_result_of_premium_levels: Result = await get_premium_levels(
            session=self.session,
            hotel_id=hotel_id,
            connected_with_rooms=connected_with_rooms,
        )
        rows_with_premium_levels = query_result_of_premium_levels.fetchall()

        premium_levels = [
            PremiumLevelVarietyDTO.model_validate(row.PremiumLevelVarietiesModel)
            for row in rows_with_premium_levels
        ]

        return premium_levels

    async def get_rooms(
        self,
        min_price_and_max_price: PriceRangeValidator,
        hotel_id: int = None,
        number_of_guests: int = None,
        services_and_levels: ServicesAndLevelsRequestSchema = None,
    ) -> list[ExtendedRoomDTO]:
        """
        Get a list of rooms in accordance with filters.

        :return: list of rooms.
        """

        query_result_of_rooms: Result = await get_rooms(
            session=self.session,
            min_price_and_max_price=min_price_and_max_price,
            hotel_id=hotel_id,
            number_of_guests=number_of_guests,
            services_and_levels=services_and_levels,
        )
        rows_with_rooms = query_result_of_rooms.fetchall()

        map_of_room_ids_and_rooms: dict[int, ExtendedRoomDTO] = {}
        for row in rows_with_rooms:
            room = ExtendedRoomDTO.model_validate(row.RoomsModel)
            room.hotel = HotelDTO.model_validate(row.HotelsModel)
            room.premium_level = (
                row.PremiumLevelVarietiesModel
                and PremiumLevelVarietyDTO.model_validate(row.PremiumLevelVarietiesModel)
            )

            room.services = []
            if row.ServiceVarietiesModel is not None:
                room.services.append(ServiceVarietyDTO.model_validate(row.ServiceVarietiesModel))

            if room.id not in map_of_room_ids_and_rooms:
                map_of_room_ids_and_rooms[room.id] = room
            else:
                map_of_room_ids_and_rooms[room.id].services.extend(room.services)

        return map_of_room_ids_and_rooms.values()
