from sqlalchemy import select, Select, func
from sqlalchemy.sql.elements import BinaryExpression

from app.db.models.hotels_model import HotelsModel
from app.db.models.rooms_model import RoomsModel
from app.db.models.hotels_services_model import HotelsServicesModel
from app.db.models.service_varieties_model import ServiceVarietiesModel

from app.services.bookings.schemas import ListOfServicesRequestSchema


def get_filters_by_services_of_hotels(
    services: ListOfServicesRequestSchema | None = None,
) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
    """
    Get sqlalchemy filters by services of hotels.

    :return: list of sqlalchemy filters.
    """

    query_filters = []
    query_having = []
    if services is not None and services.service_ids:
        query_filters.append(ServiceVarietiesModel.id.in_(services.service_ids))
        query_having.append(func.count(ServiceVarietiesModel.id) == len(services.service_ids))

    return query_filters, query_having


def get_hotels_with_requested_services_query(
    services: ListOfServicesRequestSchema | None = None,
) -> Select:
    """
    Receive inquiries from hotels that have the full requested service.

    :return: Select
    """

    query_filters, query_having = get_filters_by_services_of_hotels(services=services)

    query = (
        select(
            HotelsModel.id.label("hotel_id"),
            func.count(ServiceVarietiesModel.id).label("requested_services"),
        )
        .select_from(HotelsModel)
        .outerjoin(
            HotelsServicesModel,
            HotelsServicesModel.hotel_id == HotelsModel.id,
        )
        .outerjoin(
            ServiceVarietiesModel,
            HotelsServicesModel.service_variety_id == ServiceVarietiesModel.id,
        )
        .where(*query_filters)
        .group_by(HotelsModel.id)
        .having(*query_having)
    )

    return query


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
