from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.authorization.adapters import add_user, get_user
from app.dao.authorization.schemas import UserDTO
from app.dao.authorization.exceptions import NotExistsError

from app.services.authorization.schemas import UserRequestSchema
from app.services.check.schemas import UserAuthenticationValidator


class AuthorizationDAO:
    """
    DAO for authorization.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(
        self,
        user: UserRequestSchema,
    ) -> UserDTO:
        """
        User registration.

        :return: data of new user.
        """

        query_result_of_user: Result = await add_user(
            session=self.session,
            user=user,
        )
        row_with_user = query_result_of_user.fetchone()

        user = UserDTO.model_validate(row_with_user)

        return user

    async def get_user(
        self,
        authentication_data: UserAuthenticationValidator,
    ) -> UserDTO:
        """
        Get user by his unique field.

        :return: data of user.
        """

        query_result_of_user: Result = await get_user(
            session=self.session,
            authentication_data=authentication_data,
        )
        row_with_user = query_result_of_user.scalar_one_or_none()

        if row_with_user is None:
            raise NotExistsError(
                message="User with this email or phone number does not exist.",
                extras={
                    key: value
                    for key, value in authentication_data.model_dump().items()
                    if key is not "password" and value is not None
                },
            )

        user = UserDTO.model_validate(row_with_user)

        return user