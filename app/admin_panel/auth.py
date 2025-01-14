from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy.orm import sessionmaker
from starlette import status

from app.settings import settings

from app.db.session import async_session_maker

from app.dao.authorization.exceptions import NotExistsError

from app.services.authorization.service import AuthorizationService
from app.services.authorization.exceptions import IncorrectPasswordError
from app.services.check.schemas import UserAuthenticationValidator

from app.api.version_1.authorization.exceptions import ExpiredTokenError, InvalidTokenError, UserIsNotAdminError
from app.api.dependencies import check_is_user_admin, get_user_id


class AdminAuth(AuthenticationBackend):
    """
    Authorizer in the admin panel.
    """

    def __init__(
        self,
        session_maker: sessionmaker = async_session_maker,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.session_maker = session_maker

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

        authorization_service = AuthorizationService(session_maker=self.session_maker)

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


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY.get_secret_value())
