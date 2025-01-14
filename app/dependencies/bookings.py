from fastapi import Depends

from app.adapters.secondary.db.dao.bookings.dao import BookingDAO
from app.adapters.secondary.db.dao.transaction_manager import TransactionManager

from app.core.services.bookings.service import BookingService

from app.dependencies.base import get_transaction_manager


def get_booking_dao() -> BookingDAO:
    """
    Get booking DAO.

    :return: booking DAO.
    """

    dao = BookingDAO()

    return dao


def get_booking_service(
    transaction_manager: TransactionManager = Depends(get_transaction_manager),
    booking_dao: BookingDAO = Depends(get_booking_dao),
) -> BookingService:
    """
    Get booking service.

    :return: booking service.
    """

    service = BookingService(
        transaction_manager=transaction_manager,
        booking_dao=booking_dao,
    )

    return service
