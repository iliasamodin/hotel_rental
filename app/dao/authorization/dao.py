from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.authorization.adapters import add_user
from app.dao.authorization.schemas import UserDTO

from app.services.authorization.schemas import UserRequestSchema


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
