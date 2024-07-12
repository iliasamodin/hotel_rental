from app.web.api.base.exceptions import BaseApiError


class BaseAuthorizationApiError(BaseApiError):
    """
    Basic exception for authorization primary adapter.
    """


class TokenMissingError(BaseAuthorizationApiError):
    """
    Authorization token missing error.
    """


class InvalidTokenError(BaseAuthorizationApiError):
    """
    Authorization token verification error.
    """


class ExpiredTokenError(BaseAuthorizationApiError):
    """
    Authorization token has expired.
    """
