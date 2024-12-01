from datetime import datetime, timedelta, timezone

from jose import jwt

import bcrypt

from app.settings import settings

from app.services.authorization.schemas import UserResponseSchema, TokenResponseSchema


def get_password_hash(password: str) -> str:
    """
    Get password hash.

    :return: hash of password.
    """

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(
        password=password_bytes,
        salt=salt,
    ).decode("utf-8")

    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify user's password with password hash.

    :return: password verification success status.
    """

    plain_password_bytes = plain_password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    verification_status = bcrypt.checkpw(
        password=plain_password_bytes,
        hashed_password=hashed_password_bytes,
    )

    return verification_status


def get_access_token(
    user: UserResponseSchema,
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
) -> TokenResponseSchema:
    """
    Create and receive a token for user authorization.

    :return: authorization token.
    """

    token_expires = datetime.now(timezone.utc) + expires_delta
    data_to_encode = {
        "sub": str(user.id),
        "admin": str(int(user.is_admin)),
        "exp": token_expires,
    }
    encoded_jwt = jwt.encode(
        claims=data_to_encode,
        key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM.get_secret_value(),
    )

    access_token = TokenResponseSchema(token=encoded_jwt, expires=token_expires)

    return access_token
