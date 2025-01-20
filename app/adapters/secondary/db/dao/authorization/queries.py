from typing import Callable, Coroutine

from sqlalchemy import insert, select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

import re

from app.adapters.secondary.db.models.users_model import UsersModel

from app.adapters.secondary.db.dao.authorization.exceptions import BaseAuthorizationDAOError, AlreadyExistsError
from app.adapters.secondary.db.dao.authorization.helpers import get_filters_by_email_or_password

from app.core.services.authorization.schemas import UserRequestSchema
from app.core.services.check.schemas import UserAuthenticationValidator


async def add_user(
    session: Session | AsyncSession,
    user: UserRequestSchema,
) -> Result:
    """
    Add a user to the database
    and get the result of querying the new user's data.

    :return: result of user query.
    """

    map_of_user_data = user.model_dump()
    query = insert(UsersModel).values(map_of_user_data).returning(*UsersModel.__table__.columns)

    try:
        query_result: Result | Coroutine = session.execute(query)
        if isinstance(query_result, Coroutine):
            query_result = await query_result

    except IntegrityError as error:
        logger.error(error._message())

        # If a request to add a new user to the database fails
        #   and the cause of that error
        #   is a violation of a unique key constraint
        #   in the "users" table,
        #   then an appropriate exception will be raised
        #   and caught in the handlers
        if match_of_message := re.search(
            pattern=r"Key.*((?:email|phone)).*already exists",
            string=error._message(),
        ):
            not_unique_column = match_of_message.group(1)
            message = f"User with this {not_unique_column} already exists."

            raise AlreadyExistsError(
                message=message,
                extras={
                    not_unique_column: map_of_user_data.get(not_unique_column),
                },
            )

        else:
            raise BaseAuthorizationDAOError(
                message="Registration error at database query level.",
            )

    return query_result


async def get_user(
    session: Session | AsyncSession,
    authentication_data: UserAuthenticationValidator,
    get_query_filters: Callable = get_filters_by_email_or_password,
) -> Result:
    """
    Get the result of a query to select a user by his unique field.

    :return: result of user query.
    """

    query_filters = get_query_filters(authentication_data=authentication_data)

    query = select(UsersModel).where(*query_filters)

    query_result: Result | Coroutine = session.execute(query)
    if isinstance(query_result, Coroutine):
        query_result = await query_result

    return query_result
