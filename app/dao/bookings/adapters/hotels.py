from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression

from app.db.models.hotels_model import HotelsModel
from app.db.models.rooms_model import RoomsModel
from app.db.models.hotels_services_model import HotelsServicesModel
from app.db.models.service_varieties_model import ServiceVarietiesModel

from app.dao.bookings.helpers import get_hotels_with_requested_services_query

from app.services.bookings.schemas import ListOfServicesRequestSchema


def get_filters_for_hotels(
    location: str | None = None,
    number_of_guests: int | None = None,
    stars: int | None = None,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters for hotel query.

    :return: list of sqlalchemy filters.
    """

    query_filters = []
    if location is not None:
        query_filters.append(HotelsModel.location.ilike(f"%{location}%"))
    if number_of_guests is not None:
        query_filters.append(RoomsModel.maximum_persons >= number_of_guests)
    if stars is not None:
        query_filters.append(HotelsModel.stars == stars)

    return query_filters


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
