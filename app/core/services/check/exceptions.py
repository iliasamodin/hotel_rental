from app.core.services.base.exceptions import BaseServiceError


class BaseCheckServiceError(BaseServiceError):
    """
    Basic exception for check service.
    """


class DataValidationError(BaseCheckServiceError):
    """
    Data validation error for check service.
    """
