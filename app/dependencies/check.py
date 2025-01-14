from datetime import datetime

from app.core.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator


def get_only_for_hotels_and_only_for_rooms(
    only_for_hotels: bool = False,
    only_for_rooms: bool = False,
) -> HotelsOrRoomsValidator:
    """
    Get validator of boolean constraints to filter service's query.

    :return: scheme for limiting service query.
    """

    return HotelsOrRoomsValidator(
        only_for_hotels=only_for_hotels,
        only_for_rooms=only_for_rooms,
    )


def get_min_price_and_max_price(
    min_price: float = None,
    max_price: float = None,
) -> PriceRangeValidator:
    """
    Get a minimum and maximum price validator to filter room's query.

    :return: scheme for limiting room query.
    """

    return PriceRangeValidator(
        min_price=min_price,
        max_price=max_price,
    )


def get_min_and_max_dts(
    min_dt: datetime = None,
    max_dt: datetime = None,
) -> MinAndMaxDtsValidator:
    """
    Get validator for min and max dates.

    :return: MinAndMaxDtsValidator
    """

    return MinAndMaxDtsValidator(
        min_dt=min_dt,
        max_dt=max_dt,
    )
