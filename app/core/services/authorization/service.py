from app.ports.primary.authorization import AuthorizationServicePort
from app.ports.secondary.db.dao.authorization import AuthorizationDAOPort

from app.core.interfaces.transaction_manager import ITransactionManager
from app.core.services.authorization.dtos import UserDTO
from app.core.services.authorization.schemas import UserRequestSchema, UserResponseSchema, TokenResponseSchema
from app.core.services.authorization.helpers import get_password_hash, verify_password, get_access_token
from app.core.services.authorization.exceptions import IncorrectPasswordError
from app.core.services.check.schemas import UserAuthenticationValidator


class AuthorizationService(AuthorizationServicePort):
    """
    Class of service for authorization.
    """

    def __init__(
        self,
        transaction_manager: ITransactionManager,
        authorization_dao: AuthorizationDAOPort,
    ):
        self.transaction_manager = transaction_manager
        self.authorization_dao = authorization_dao

    async def registration(
        self,
        user: UserRequestSchema,
    ) -> UserResponseSchema:
        """
        User registration.

        :return: data of new user.
        """

        user.password = get_password_hash(password=user.password)

        async with self.transaction_manager(self.authorization_dao) as session_id:
            user_dto: UserDTO = await self.authorization_dao.add_user(user=user)

            await self.transaction_manager.commit(session_id=session_id)

            user = UserResponseSchema(
                id=user_dto.id,
                email=user_dto.email,
                phone=user_dto.phone,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
                is_admin=user_dto.is_admin,
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

        async with self.transaction_manager(self.authorization_dao):
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
                is_admin=user_dto.is_admin,
            )
            access_token: TokenResponseSchema = get_access_token(user=user)

        return access_token
