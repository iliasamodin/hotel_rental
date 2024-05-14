from sqlalchemy.sql.elements import BinaryExpression

from app.db.models.users_model import UsersModel

from app.services.check.schemas import UserAuthenticationValidator


def get_filters_by_email_or_password(
    authentication_data: UserAuthenticationValidator,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters by email or password of user.

    :return: list of sqlalchemy filters.
    """

    query_filters = []
    if authentication_data.email is not None:
        query_filters.append(UsersModel.email == authentication_data.email)
    if authentication_data.phone is not None:
        query_filters.append(UsersModel.phone == authentication_data.phone)

    return query_filters
