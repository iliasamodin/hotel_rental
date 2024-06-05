from sqlalchemy.orm import sessionmaker

from app.dao.authorization.dao import AuthorizationDAO
from app.dao.authorization.schemas import UserDTO

from app.services.authorization.schemas import UserRequestSchema, UserResponseSchema, TokenResponseSchema
from app.services.authorization.helpers import get_password_hash, verify_password, get_access_token
from app.services.authorization.exceptions import IncorrectPasswordError
from app.services.check.schemas import UserAuthenticationValidator


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
            user_dto: UserDTO = await self.authorization_dao.add_user(user=user)

            user = UserResponseSchema(
                id=user_dto.id,
                email=user_dto.email,
                phone=user_dto.phone,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
            )

        return user

    async def authentication(
        self,
        authentication_data: UserAuthenticationValidator,
    ) -> TokenResponseSchema:
        """
        User authentication.

        :return: authorization token.
        """

        async with self.session_maker.begin() as session:
            self.authorization_dao = AuthorizationDAO(session=session)
            user_dto: UserDTO = await self.authorization_dao.get_user(authentication_data=authentication_data)

            if not verify_password(
                plain_password=authentication_data.password,
                hashed_password=user_dto.password,
            ):
                raise IncorrectPasswordError(
                    message="Invalid password.",
                    extras={
                        "password": authentication_data.password,
                    },
                )

            user = UserResponseSchema(
                id=user_dto.id,
                email=user_dto.email,
                phone=user_dto.phone,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
            )
            access_token: TokenResponseSchema = get_access_token(user=user)

        return access_token
