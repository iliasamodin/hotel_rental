from app.ports.primary.authorization import AuthorizationServicePort
from app.ports.secondary.db.dao.authorization import AuthorizationDAOPort

from app.core.interfaces.transaction_context import IStaticAsyncTransactionContextFactory
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
        transaction_context_factory: IStaticAsyncTransactionContextFactory,
        authorization_dao: AuthorizationDAOPort,
    ):
        self.transaction_context_factory = transaction_context_factory
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

        transaction_context = self.transaction_context_factory.init_transaction_context()
        async with transaction_context():
            user_dto: UserDTO = await self.authorization_dao.add_user(
                transaction_context=transaction_context,
                user=user,
            )

            await transaction_context.commit()

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

        transaction_context = self.transaction_context_factory.init_transaction_context()
        async with transaction_context():
            user_dto: UserDTO = await self.authorization_dao.get_user(
                transaction_context=transaction_context,
                authentication_data=authentication_data,
            )

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
