from fastapi import Depends

from app.adapters.secondary.db.dao.bookings.dao import BookingDAO
from app.adapters.secondary.db.dao.transaction_context import StaticAsyncTransactionContextFactory

from app.core.services.bookings.service import BookingService

from app.dependencies.base import get_transaction_context_factory


def get_booking_dao() -> BookingDAO:
    """
    Get booking DAO.

    :return: booking DAO.
    """

    dao = BookingDAO()

    return dao


def get_booking_service(
    transaction_context_factory: StaticAsyncTransactionContextFactory = Depends(get_transaction_context_factory),
    booking_dao: BookingDAO = Depends(get_booking_dao),
) -> BookingService:
    """
    Get booking service.

    :return: booking service.
    """

    service = BookingService(
        transaction_context_factory=transaction_context_factory,
        booking_dao=booking_dao,
    )

    return service
