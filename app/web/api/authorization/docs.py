from enum import Enum

from app.services.authorization.schemas import UserResponseSchema, TokenResponseSchema

from app.web.api.base.schemas import BaseErrorResponseSchema


class RegistrationEnum(Enum):
    """
    Scheme of responses to a user registration request.
    """

    SUCCESS: UserResponseSchema = UserResponseSchema(
        id=1,
        email="user@example.com",
        phone="+7-999-999-99-99",
        first_name="Till",
        last_name="Lindemann",
    )
    NOT_UNIQUE_FIELD_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="User with this email already exists.",
        extras={
            "email": "user@example.com",
        }
    )
    DAO_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Registration error at database query level.",
        extras=None,
    )
    SERVER_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Unspecified error.",
        extras={
            "doc": "Exception documentation."
        },
    )


class AuthenticationEnum(Enum):
    """
    Scheme of responses to a user authentication request.
    """

    SUCCESS: TokenResponseSchema = TokenResponseSchema(
        token="Authorization token",
        expires="1970-01-01T00:00:00Z",
    )
    NOT_EXISTS_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="User with this email or phone number does not exist.",
        extras={
            "email": "user@example.com",
        },
    )
    INVALID_PASSWORD_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Invalid password.",
        extras={
            "password": "Password",
        },
    )
    SERVER_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Unspecified error.",
        extras={
            "doc": "Exception documentation."
        },
    )
