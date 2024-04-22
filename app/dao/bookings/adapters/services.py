from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.hotels_services_model import HotelsServicesModel
from app.db.models.rooms_services_model import RoomsServicesModel
from app.db.models.service_varieties_model import ServiceVarietiesModel

from app.services.check.schemas import HotelsOrRoomsValidator


async def get_services(
    session: AsyncSession,
    boolean_constraints_for_filters: HotelsOrRoomsValidator,
) -> Result:
    """
    Get the result of a hotel services query from the database.

    :return: result of a hotel services query.
    """

    query = (
        select(ServiceVarietiesModel)
        .select_from(ServiceVarietiesModel)
        .distinct(ServiceVarietiesModel.id)
    )

    if boolean_constraints_for_filters.only_for_hotels:
        query = query.join(
            HotelsServicesModel,
            HotelsServicesModel.service_variety_id == ServiceVarietiesModel.id
        )
    elif boolean_constraints_for_filters.only_for_rooms:
        query = query.join(
            RoomsServicesModel,
            RoomsServicesModel.service_variety_id == ServiceVarietiesModel.id
        )

    query.order_by(ServiceVarietiesModel.id)

    query_result = await session.execute(query)

    return query_result
