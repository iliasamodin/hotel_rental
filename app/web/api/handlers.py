from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from app.dao.base.exceptions import BaseDAOError
from app.dao.authorization.exceptions import AlreadyExistsError

from app.services.base.exceptions import BaseServiceError
from app.services.check.exceptions import BaseCheckServiceError


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

    @app.exception_handler(BaseServiceError)
    async def _exception(request: Request, exc: BaseServiceError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
