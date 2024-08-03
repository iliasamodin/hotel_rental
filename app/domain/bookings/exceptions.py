from app.domain.base.exceptions import BaseDomainError


class BaseBookingDomainError(BaseDomainError):
    """
    Basic exception for booking domain.
    """


class RoomCapacityError(BaseBookingDomainError):
    """
    Error in room capacity in number of persons.
    """
