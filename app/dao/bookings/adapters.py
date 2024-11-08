from typing import Callable, Coroutine

from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.bookings_model import BookingsModel
from app.db.models.hotels_services_model import HotelsServicesModel
from app.db.models.images_model import ImagesModel
from app.db.models.rooms_services_model import RoomsServicesModel
from app.db.models.service_varieties_model import ServiceVarietiesModel
from app.db.models.hotels_model import HotelsModel
from app.db.models.rooms_model import RoomsModel
from app.db.models.premium_level_varieties_model import PremiumLevelVarietiesModel

from app.dao.bookings.helpers import (
    get_filters_for_bookings,
    get_hotels_with_requested_services_query,
    get_filters_for_hotels,
    get_rooms_with_requested_services_and_levels_query,
    get_filters_for_rooms,
)

from app.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator


async def get_services(
    session: Session | AsyncSession,
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

    query_result: Result | Coroutine = session.execute(query)
    if isinstance(query_result, Coroutine):
        query_result = await query_result

    return query_result


async def get_hotels(
    session: Session | AsyncSession,
    location: str | None = None,
    number_of_guests: int | None = None,
    stars: int | None = None,
    services: list[int] | None = None,
    get_query_filters: Callable = get_filters_for_hotels,
) -> Result:
    """
    Get the result of a hotel query from the database.

    :return: result of a hotel query.
    """

    hotels_with_requested_services_sbq = get_hotels_with_requested_services_query(services=services).subquery()

    window_of_count_rooms = {
        "partition_by": (HotelsModel.id, ServiceVarietiesModel.id),
    }

    query_filters = get_query_filters(
        location=location,
        number_of_guests=number_of_guests,
        stars=stars,
    )

    query = (
        select(
            HotelsModel,
            ServiceVarietiesModel,
            func.count(RoomsModel.id).over(**window_of_count_rooms).label("rooms_quantity"),
            ImagesModel,
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
        .outerjoin(
            ImagesModel,
            HotelsModel.main_image_id == ImagesModel.id,
        )
        .where(*query_filters)
        .order_by(HotelsModel.id, ServiceVarietiesModel.id)
    )

    query_result: Result | Coroutine = session.execute(query)
    if isinstance(query_result, Coroutine):
        query_result = await query_result

    return query_result


async def get_premium_levels(
    session: Session | AsyncSession,
    hotel_id: int | None = None,
    connected_with_rooms: bool = False,
) -> Result:
    """
    Get result of query for premium levels from database.

    :return: result of query for premium levels.
    """

    query = (
        select(PremiumLevelVarietiesModel)
        .select_from(PremiumLevelVarietiesModel)
        .distinct(PremiumLevelVarietiesModel.id)
    )

    if hotel_id is not None:
        query = (
            query
            .join(
                RoomsModel,
                RoomsModel.premium_level_id == PremiumLevelVarietiesModel.id
            )
            .join(
                HotelsModel,
                RoomsModel.hotel_id == HotelsModel.id,
            )
            .where(HotelsModel.id == hotel_id)
        )
    elif connected_with_rooms:
        query = query.join(
            RoomsModel,
            RoomsModel.premium_level_id == PremiumLevelVarietiesModel.id
        )

    query.order_by(PremiumLevelVarietiesModel.id)

    query_result: Result | Coroutine = session.execute(query)
    if isinstance(query_result, Coroutine):
        query_result = await query_result

    return query_result


async def get_rooms(
    session: Session | AsyncSession,
    min_price_and_max_price: PriceRangeValidator,
    hotel_id: int = None,
    number_of_guests: int = None,
    services: list[int] | None = None,
    premium_levels: list[int] | None = None,
    get_query_filters: Callable = get_filters_for_rooms,
) -> Result:
    """
    Get the result of a room query from the database.

    :return: result of a room query.
    """

    rooms_with_requested_services_sbq = get_rooms_with_requested_services_and_levels_query(
        services=services,
        premium_levels=premium_levels,
    ).subquery()

    query_filters = get_query_filters(
        min_price_and_max_price=min_price_and_max_price,
        hotel_id=hotel_id,
        number_of_guests=number_of_guests,
    )

    query = (
        select(
            RoomsModel,
            HotelsModel,
            PremiumLevelVarietiesModel,
            ServiceVarietiesModel,
        )
        .select_from(RoomsModel)
        .join(
            HotelsModel,
            RoomsModel.hotel_id == HotelsModel.id
        )
        .join(
            rooms_with_requested_services_sbq,
            rooms_with_requested_services_sbq.c.room_id == RoomsModel.id,
        )
        .outerjoin(
            PremiumLevelVarietiesModel,
            RoomsModel.premium_level_id == PremiumLevelVarietiesModel.id,
        )
        .outerjoin(
            RoomsServicesModel,
            RoomsServicesModel.room_id == RoomsModel.id,
        )
        .outerjoin(
            ServiceVarietiesModel,
            RoomsServicesModel.service_variety_id == ServiceVarietiesModel.id,
        )
        .where(*query_filters)
        .order_by(RoomsModel.id)
    )

    query_result: Result | Coroutine = session.execute(query)
    if isinstance(query_result, Coroutine):
        query_result = await query_result

    return query_result


async def get_bookings(
    session: Session | AsyncSession,
    min_and_max_dts: MinAndMaxDtsValidator,
    number_of_guests: int = None,
    user_id: int | None = None,
    room_id: int | None = None,
    get_query_filters: Callable = get_filters_for_bookings,
) -> Result:
    """
    Get the result of query for user's bookings from the database.

    :return: result of a booking query.
    """

    query_filters = get_query_filters(
        user_id=user_id,
        min_and_max_dts=min_and_max_dts,
        number_of_guests=number_of_guests,
        room_id=room_id,
    )

    query = (
        select(
            BookingsModel,
            RoomsModel,
        )
        .select_from(BookingsModel)
        .join(
            RoomsModel,
            BookingsModel.room_id == RoomsModel.id,
        )
        .where(*query_filters)
        .order_by(BookingsModel.id)
    )

    query_result: Result | Coroutine = session.execute(query)
    if isinstance(query_result, Coroutine):
        query_result = await query_result

    return query_result
