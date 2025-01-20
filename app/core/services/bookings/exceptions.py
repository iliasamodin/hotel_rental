from app.core.services.base.exceptions import BaseServiceError


class BaseBookingServiceError(BaseServiceError):
    """
    Basic exception for booking service.
    """


class RoomAlreadyBookedError(BaseBookingServiceError):
    """
    Error booking a room for a date
    for which this room is already booked.
    """
