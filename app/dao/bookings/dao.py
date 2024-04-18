from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.bookings.adapters.services import get_services
from app.dao.bookings.schemas import ServiceVarietyDTO

from app.services.check.schemas import HotelsOrRoomsValidator


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
