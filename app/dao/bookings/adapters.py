from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.hotels_services_model import HotelsServicesModel
from app.db.models.rooms_services_model import RoomsServicesModel
from app.db.models.service_varieties_model import ServiceVarietiesModel
from app.db.models.hotels_model import HotelsModel
from app.db.models.rooms_model import RoomsModel

from app.dao.bookings.helpers import get_hotels_with_requested_services_query, get_filters_for_hotels

from app.services.check.schemas import HotelsOrRoomsValidator
from app.services.bookings.schemas import ListOfServicesRequestSchema


async def get_services(
    session: AsyncSession,
    only_for_hotels_and_only_for_rooms: HotelsOrRoomsValidator,
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

    if only_for_hotels_and_only_for_rooms.only_for_hotels:
        query = query.join(
            HotelsServicesModel,
            HotelsServicesModel.service_variety_id == ServiceVarietiesModel.id
        )
    elif only_for_hotels_and_only_for_rooms.only_for_rooms:
        query = query.join(
            RoomsServicesModel,
            RoomsServicesModel.service_variety_id == ServiceVarietiesModel.id
        )

    query.order_by(ServiceVarietiesModel.id)

    query_result = await session.execute(query)

    return query_result


async def get_hotels(
    session: AsyncSession,
    location: str | None = None,
    number_of_guests: int | None = None,
    stars: int | None = None,
    services: ListOfServicesRequestSchema | None = None,
) -> Result:
    """
    Get the result of a hotel query from the database.

    :return: result of a hotel query.
    """

    hotels_with_requested_services_sbq = get_hotels_with_requested_services_query(services=services).subquery()

    window_of_count_rooms = {
        "partition_by": (HotelsModel.id, ServiceVarietiesModel.id),
    }

    query_filters = get_filters_for_hotels(
        location=location,
        number_of_guests=number_of_guests,
        stars=stars,
    )

    query = (
        select(
            HotelsModel,
            ServiceVarietiesModel,
            func.count(RoomsModel.id).over(**window_of_count_rooms).label("rooms_quantity"),
        )
        .select_from(HotelsModel)
        .distinct(HotelsModel.id, ServiceVarietiesModel.id)
        .join(
            RoomsModel,
            RoomsModel.hotel_id == HotelsModel.id,
        )
        .join(
            hotels_with_requested_services_sbq,
            hotels_with_requested_services_sbq.c.hotel_id == HotelsModel.id,
        )
        .outerjoin(
            HotelsServicesModel,
            HotelsServicesModel.hotel_id == HotelsModel.id,
        )
        .outerjoin(
            ServiceVarietiesModel,
            HotelsServicesModel.service_variety_id == ServiceVarietiesModel.id,
        )
        .where(*query_filters)
        .order_by(HotelsModel.id, ServiceVarietiesModel.id)
    )

    query_result = await session.execute(query)

    return query_result
