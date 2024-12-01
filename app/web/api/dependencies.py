from datetime import datetime

from fastapi import Depends, Request
from jose import jwt, JWTError

from app.settings import settings

from app.web.api.authorization.exceptions import (
    TokenMissingError,
    InvalidTokenError,
    ExpiredTokenError,
    UserIsNotAdminError,
)


def get_access_token(request: Request) -> str:
    """
    Get authorization token from cookies of user's request.

    :return: authorization token.
    """

    access_token = request.cookies.get(settings.ACCESS_TOKEN_COOKIE)
    if access_token is None:
        raise TokenMissingError(message="Access token missing from cookies.")

    return access_token


def get_user_id(access_token: str = Depends(get_access_token)) -> int:
    """
    Get the ID of the user who sent the request.

    :return: user ID.
    """

    try:
        token_payload = jwt.decode(
            token=access_token,
            key=settings.SECRET_KEY.get_secret_value(),
            algorithms=settings.ALGORITHM.get_secret_value(),
        )

        token_expires = int(token_payload["exp"])
        user_id = int(token_payload["sub"])

    except (
        JWTError,
        KeyError,
        ValueError,
    ):
        raise InvalidTokenError(message=f"Invalid access token {access_token}.")

    if (token_expires := datetime.fromtimestamp(timestamp=token_expires)) < datetime.now():
        raise ExpiredTokenError(message=f"Access token has expired {token_expires}.")

    return user_id


def check_is_user_admin(access_token: str = Depends(get_access_token)) -> bool:
    """
    Check if the user is an admin.

    :return: admin status.
    """

    try:
        token_payload = jwt.decode(
            token=access_token,
            key=settings.SECRET_KEY.get_secret_value(),
            algorithms=settings.ALGORITHM.get_secret_value(),
        )

        is_admin = bool(int(token_payload["admin"]))

    except (
        JWTError,
        KeyError,
        ValueError,
    ):
        raise InvalidTokenError(message=f"Invalid access token {access_token}.")

    if not is_admin:
        raise UserIsNotAdminError(
            message="The user doesn't have rights to access the resource because he is not an administrator.",
        )

    return is_admin
