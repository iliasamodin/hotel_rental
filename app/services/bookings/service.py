from sqlalchemy.orm import sessionmaker

from app.dao.bookings.dao import BookingDAO
from app.dao.bookings.schemas import ServiceVarietyDTO

from app.services.bookings.schemas import ServiceVarietyResponseSchema
from app.services.check.schemas import HotelsOrRoomsValidator


class BookingService:
    """
    Class of service for booking.
    """

    booking_dao: BookingDAO

    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    async def get_services(
        self,
        boolean_constraints_for_filters: HotelsOrRoomsValidator,
    ) -> list[ServiceVarietyResponseSchema]:
        """
        Get all service options.

        :return: list of services.
        """

        async with self.session_maker.begin() as session:
            self.booking_dao = BookingDAO(session=session)
            services_dto: list[ServiceVarietyDTO] = await self.booking_dao.get_services(
                boolean_constraints_for_filters=boolean_constraints_for_filters,
            )

            services = [
                ServiceVarietyResponseSchema(
                    id=service.id,
                    key=service.key,
                    name=service.name,
                    desc=service.desc,
                )
                for service in services_dto
            ]

        return services
