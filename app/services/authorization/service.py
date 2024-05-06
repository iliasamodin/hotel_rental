from sqlalchemy.orm import sessionmaker

from app.dao.authorization.dao import AuthorizationDAO

from app.services.authorization.schemas import UserRequestSchema, UserResponseSchema
from app.services.authorization.helpers import get_password_hash


class AuthorizationService:
    """
    Class of service for authorization.
    """

    authorization_dao: AuthorizationDAO

    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    async def registration(
        self,
        user: UserRequestSchema,
    ) -> UserResponseSchema:
        """
        User registration.

        :return: data of new user.
        """

        user.password = get_password_hash(password=user.password)

        async with self.session_maker.begin() as session:
            self.authorization_dao = AuthorizationDAO(session=session)
            user_dao = await self.authorization_dao.add_user(user=user)

            user = UserResponseSchema(
                id=user_dao.id,
                email=user_dao.email,
                phone=user_dao.phone,
                first_name=user_dao.first_name,
                last_name=user_dao.last_name,
            )

            return user
