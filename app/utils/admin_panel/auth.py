from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette import status

from app.settings import settings

from app.adapters.secondary.db.dao.authorization.exceptions import NotExistsError
from app.adapters.secondary.db.dao.transaction_context import StaticAsyncTransactionContextFactory
from app.adapters.secondary.db.session import async_session_maker

from app.core.interfaces.transaction_context import IStaticAsyncTransactionContextFactory
from app.core.services.authorization.service import AuthorizationService
from app.core.services.authorization.exceptions import IncorrectPasswordError
from app.core.services.check.schemas import UserAuthenticationValidator

from app.adapters.primary.api.version_1.authorization.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    UserIsNotAdminError,
)

from app.dependencies.auth import check_is_user_admin, get_user_id


class AdminAuth(AuthenticationBackend):
    """
    Authorizer in the admin panel.
    """

    def __init__(
        self,
        transaction_context_factory: IStaticAsyncTransactionContextFactory,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.transaction_context_factory = transaction_context_factory

    async def login(self, request: Request) -> bool:
        """
        Login to the admin panel and access token generation.

        :return: login status.
        """

        form = await request.form()
        authentication_data = UserAuthenticationValidator(
            email=form.get("username"),
            password=form.get("password"),
        )

        authorization_service = AuthorizationService(
            transaction_context_factory=self.transaction_context_factory,
        )

        try:
            access_token = await authorization_service.authentication(authentication_data=authentication_data)

        except (IncorrectPasswordError, NotExistsError):
            return RedirectResponse(
                url=f"{settings.ADMIN_PANEL_BASE_URL}/login",
                status_code=status.HTTP_302_FOUND,
            )

        request.session.update({settings.ADMIN_PANEL_ACCESS_TOKEN_COOKIE: access_token.token})

        return True

    async def logout(self, request: Request) -> bool:
        """
        Logging out of the admin panel account by clear the session.

        :return: logout status.
        """

        request.session.clear()

        return True

    async def authenticate(self, request: Request) -> bool:
        """
        Authentication in the admin panel of application.

        :return: authentication status.
        """

        access_token = request.session.get(settings.ADMIN_PANEL_ACCESS_TOKEN_COOKIE)

        if not access_token:
            return False

        try:
            get_user_id(access_token=access_token)
            is_admin = check_is_user_admin(access_token=access_token)

        except (InvalidTokenError, ExpiredTokenError, UserIsNotAdminError):
            return False

        return is_admin


authentication_backend = AdminAuth(
    transaction_context_factory=StaticAsyncTransactionContextFactory(session_maker=async_session_maker),
    secret_key=settings.SECRET_KEY.get_secret_value(),
)
