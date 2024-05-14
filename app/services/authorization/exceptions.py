from app.services.base.exceptions import BaseServiceError


class BaseAuthorizationServiceError(BaseServiceError):
    """
    Basic exception for authorization service.
    """


class IncorrectPasswordError(BaseAuthorizationServiceError):
    """
    User password verification error.
    """
