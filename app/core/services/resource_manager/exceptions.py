from app.core.services.base.exceptions import BaseServiceError


class BaseResourceManagerServiceError(BaseServiceError):
    """
    Basic exception for resource manager service.
    """


class EntityNotExistsError(BaseResourceManagerServiceError):
    """
    Error getting a non-existent entity.
    """
