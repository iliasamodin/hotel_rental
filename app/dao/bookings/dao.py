from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.bookings.adapters.services import get_services
from app.dao.bookings.adapters.hotels import get_hotels
from app.dao.bookings.schemas import ServiceVarietyDTO, ExtendedHotelDTO

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
        boolean_constraints_for_filters: HotelsOrRoomsValidator,
    ) -> list[ServiceVarietyDTO]:
        """
        Get all service options.

        :return: list of services.
        """

        query_result_of_services = await get_services(
            session=self.session,
            boolean_constraints_for_filters=boolean_constraints_for_filters,
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

        query_result_of_hotels = await get_hotels(
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
