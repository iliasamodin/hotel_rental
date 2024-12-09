from app.domain.base.exceptions import BaseDomainError


class BaseBookingDomainError(BaseDomainError):
    """
    Basic exception for booking domain.
    """


class RentalPeriodError(BaseBookingDomainError):
    """
    Error in the length of the rental period.
    """


class RoomCapacityError(BaseBookingDomainError):
    """
    Error in room capacity in number of persons.
    """


class RoomAlreadyBookedError(BaseBookingDomainError):
    """
    Error booking a room for a date
    for which this room is already booked.
    """


class ItemNotExistsError(BaseBookingDomainError):
    """
    Error deleting a non-existent item.
    """


class ItemNotBelongUserError(BaseBookingDomainError):
    """
    Error that the item does not belong to the user.
    """


class DeletionTimeEndedError(BaseBookingDomainError):
    """
    The time interval
    when deletion was available for this item has ended.
    """
