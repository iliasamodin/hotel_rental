from sqlalchemy import or_, select, Select, func, between
from sqlalchemy.sql.elements import BinaryExpression

from app.adapters.secondary.db.models.bookings_model import BookingsModel
from app.adapters.secondary.db.models.hotels_model import HotelsModel
from app.adapters.secondary.db.models.rooms_model import RoomsModel
from app.adapters.secondary.db.models.hotels_services_model import HotelsServicesModel
from app.adapters.secondary.db.models.service_varieties_model import ServiceVarietiesModel
from app.adapters.secondary.db.models.rooms_services_model import RoomsServicesModel

from app.core.services.check.schemas import MinAndMaxDtsValidator, PriceRangeValidator


def get_filters_by_services(
    services: list[int] | None = None,
    *args,
    **kwargs,
) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
    """
    Get sqlalchemy filters by services of hotels or rooms.

    :return: filters and havings.
    """

    query_filters = []
    query_having = []
    if services:
        query_filters.append(ServiceVarietiesModel.id.in_(services))
        query_having.append(func.count(ServiceVarietiesModel.id) == len(services))

    return query_filters, query_having


def get_hotels_with_requested_services_query(
    services: list[int] | None = None,
    *args,
    **kwargs,
) -> Select:
    """
    Get a query to select hotel identifiers
    that have a complete list of service options
    from those that were passed to the function.

    :return: query to select hotel identifiers.
    """

    query_filters, query_having = get_filters_by_services(services=services)

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
    *args,
    **kwargs,
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


def get_filters_by_premium_levels(
    premium_levels: list[int] | None = None,
    *args,
    **kwargs,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters by premium levels of rooms.

    :return: list of sqlalchemy filters.
    """

    query_filters = []
    if premium_levels:
        query_filters.append(RoomsModel.premium_level_id.in_(premium_levels))

    return query_filters


def get_rooms_with_requested_services_and_levels_query(
    services: list[int] | None = None,
    premium_levels: list[int] | None = None,
    *args,
    **kwargs,
) -> Select:
    """
    Get a query to select room identifiers
    that have a complete list of service options
    from those that were passed to the function
    and have a premium level from the list of levels.

    :return: query to select room identifiers.
    """

    query_filters, query_having = get_filters_by_services(services=services)
    query_filters += get_filters_by_premium_levels(
        premium_levels=premium_levels,
    )

    query = (
        select(
            RoomsModel.id.label("room_id"),
            RoomsModel.premium_level_id,
            func.count(ServiceVarietiesModel.id).label("requested_services"),
        )
        .select_from(RoomsModel)
        .outerjoin(
            RoomsServicesModel,
            RoomsServicesModel.room_id == RoomsModel.id,
        )
        .outerjoin(
            ServiceVarietiesModel,
            RoomsServicesModel.service_variety_id == ServiceVarietiesModel.id,
        )
        .where(*query_filters)
        .group_by(RoomsModel.id)
        .having(*query_having)
    )

    return query


def get_filters_for_rooms(
    min_price_and_max_price: PriceRangeValidator,
    hotel_id: int = None,
    number_of_guests: int = None,
    *args,
    **kwargs,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters for hotel query.

    :return: list of sqlalchemy filters.
    """

    query_filters = []
    if min_price_and_max_price.min_price is not None:
        query_filters.append(RoomsModel.price >= min_price_and_max_price.min_price)
    if min_price_and_max_price.max_price is not None:
        query_filters.append(RoomsModel.price <= min_price_and_max_price.max_price)
    if hotel_id is not None:
        query_filters.append(HotelsModel.id == hotel_id)
    if number_of_guests is not None:
        query_filters.append(RoomsModel.maximum_persons >= number_of_guests)

    return query_filters


def get_filters_for_bookings(
    min_and_max_dts: MinAndMaxDtsValidator,
    number_of_guests: int = None,
    user_id: int | None = None,
    room_id: int | None = None,
    *args,
    **kwargs,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters for booking query.

    :return: list of sqlalchemy filters.
    """

    query_filters = []
    if user_id is not None:
        query_filters.append(BookingsModel.user_id == user_id)
    if min_and_max_dts.min_dt is not None:
        query_filters.append(BookingsModel.check_in_dt >= min_and_max_dts.min_dt)
    if min_and_max_dts.max_dt is not None:
        query_filters.append(BookingsModel.check_in_dt <= min_and_max_dts.max_dt)
    if number_of_guests is not None:
        query_filters.append(BookingsModel.number_of_persons == number_of_guests)
    if room_id is not None:
        query_filters.append(BookingsModel.room_id == room_id)

    return query_filters


def get_filters_for_booking_overlaps(
    min_and_max_dts: MinAndMaxDtsValidator,
    room_id: int | None = None,
    *args,
    **kwargs,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters for booking overlap query.

    :return: list of sqlalchemy filters.
    """

    filters_by_or = []
    if min_and_max_dts.min_dt is not None:
        filters_by_or.append(
            between(
                min_and_max_dts.min_dt,
                BookingsModel.check_in_dt,
                BookingsModel.check_out_dt,
            )
        )
    if min_and_max_dts.max_dt is not None:
        filters_by_or.append(
            between(
                min_and_max_dts.max_dt,
                BookingsModel.check_in_dt,
                BookingsModel.check_out_dt,
            )
        )
    if min_and_max_dts.min_dt is not None and min_and_max_dts.max_dt is not None:
        filters_by_or.append(
            between(
                BookingsModel.check_in_dt,
                min_and_max_dts.min_dt,
                min_and_max_dts.max_dt,
            )
        )
        filters_by_or.append(
            between(
                BookingsModel.check_out_dt,
                min_and_max_dts.min_dt,
                min_and_max_dts.max_dt,
            )
        )

    query_filters = [or_(*filters_by_or)]
    if room_id is not None:
        query_filters.append(BookingsModel.room_id == room_id)

    return query_filters
