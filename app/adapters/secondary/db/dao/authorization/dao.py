from typing import Coroutine

from sqlalchemy.engine import Result

from app.ports.secondary.db.dao.authorization import AuthorizationDAOPort

from app.adapters.secondary.db.dao.base.dao import BaseDAO
from app.adapters.secondary.db.dao.authorization.queries import add_user, get_user
from app.adapters.secondary.db.dao.authorization.exceptions import NotExistsError

from app.core.interfaces.transaction_context import IStaticSyncTransactionContext
from app.core.services.authorization.dtos import UserDTO
from app.core.services.authorization.schemas import UserRequestSchema
from app.core.services.check.schemas import UserAuthenticationValidator


class AuthorizationDAO(BaseDAO, AuthorizationDAOPort):
    """
    DAO for authorization.
    """

    async def add_user(
        self,
        transaction_context: IStaticSyncTransactionContext,
        user: UserRequestSchema,
    ) -> UserDTO:
        """
        User registration.

        :return: data of new user.
        """

        query_result_of_user: Result | Coroutine = add_user(
            session=transaction_context.session,
            user=user,
        )
        if isinstance(query_result_of_user, Coroutine):
            query_result_of_user = await query_result_of_user

        row_with_user = query_result_of_user.fetchone()

        user = UserDTO.model_validate(row_with_user)

        return user

    async def get_user(
        self,
        transaction_context: IStaticSyncTransactionContext,
        authentication_data: UserAuthenticationValidator,
    ) -> UserDTO:
        """
        Get user by his unique field.

        :return: data of user.
        """

        query_result_of_user: Result | Coroutine = get_user(
            session=transaction_context.session,
            authentication_data=authentication_data,
        )
        if isinstance(query_result_of_user, Coroutine):
            query_result_of_user = await query_result_of_user

        row_with_user = query_result_of_user.scalar_one_or_none()

        if row_with_user is None:
            raise NotExistsError(
                message="User with this email or phone number does not exist.",
                extras={
                    key: value
                    for key, value in authentication_data.model_dump().items()
                    if key != "password" and value is not None
                },
            )

        user = UserDTO.model_validate(row_with_user)

        return user
