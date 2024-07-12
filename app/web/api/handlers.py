from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from app.dao.base.exceptions import BaseDAOError
from app.dao.authorization.exceptions import AlreadyExistsError, NotExistsError

from app.services.base.exceptions import BaseServiceError
from app.services.check.exceptions import BaseCheckServiceError
from app.services.authorization.exceptions import IncorrectPasswordError

from app.web.api.base.exceptions import BaseApiError
from app.web.api.authorization.exceptions import BaseAuthorizationApiError


def registering_exception_handlers(app: FastAPI):
    """
    Registering handlers for custom exceptions.
    """

    @app.exception_handler(AlreadyExistsError)
    async def _exception(request: Request, exc: AlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )

    @app.exception_handler(NotExistsError)
    async def _exception(request: Request, exc: NotExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )

    @app.exception_handler(BaseDAOError)
    async def _exception(request: Request, exc: BaseDAOError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )

    @app.exception_handler(BaseCheckServiceError)
    async def _exception(request: Request, exc: BaseCheckServiceError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )

    @app.exception_handler(IncorrectPasswordError)
    async def _exception(request: Request, exc: IncorrectPasswordError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )

    @app.exception_handler(BaseServiceError)
    async def _exception(request: Request, exc: BaseServiceError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )

    @app.exception_handler(BaseAuthorizationApiError)
    async def _exception(request: Request, exc: BaseAuthorizationApiError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )

    @app.exception_handler(BaseApiError)
    async def _exception(request: Request, exc: BaseApiError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )

    @app.exception_handler(Exception)
    async def _exception(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Unspecified error.",
                "extras": {
                    "doc": exc.__doc__,
                },
            },
        )
