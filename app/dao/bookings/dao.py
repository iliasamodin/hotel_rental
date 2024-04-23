from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.bookings.adapters import get_services, get_hotels, get_premium_levels
from app.dao.bookings.schemas import ServiceVarietyDTO, ExtendedHotelDTO, PremiumLevelVarietyDTO

from app.services.check.schemas import HotelsOrRoomsValidator
from app.services.bookings.schemas import ListOfServicesRequestSchema


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

        map_of_hotels_services: dict[int, ExtendedHotelDTO] = {}
        for row in rows_with_hotels:
            hotel = ExtendedHotelDTO.model_validate(row.HotelsModel)
            hotel.rooms_quantity = row.rooms_quantity
            hotel.services = []
            if row.ServiceVarietiesModel is not None:
                hotel.services.append(ServiceVarietyDTO.model_validate(row.ServiceVarietiesModel))

            if hotel.id not in map_of_hotels_services:
                map_of_hotels_services[hotel.id] = hotel
            else:
                map_of_hotels_services[hotel.id].services.extend(hotel.services)

        return map_of_hotels_services.values()

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
