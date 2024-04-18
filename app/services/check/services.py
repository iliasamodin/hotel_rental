from sqlalchemy.orm import sessionmaker

from app.db.session import get_async_session_maker

from app.services.check.schemas import HotelsOrRoomsValidator


def get_session_maker() -> sessionmaker:
    """
    Get session-maker.

    :return: sessionmaker
    """

    return get_async_session_maker()


def get_only_for_hotels_and_only_for_rooms(
    only_for_hotels: bool = False,
    only_for_rooms: bool = False,
) -> HotelsOrRoomsValidator:
    """
    Get validator of boolean constraints for list of query's filters.

    :return: HotelsOrRoomsValidator
    """

    return HotelsOrRoomsValidator(
        only_for_hotels=only_for_hotels,
        only_for_rooms=only_for_rooms,
    )
