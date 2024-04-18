from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.services.check.exceptions import BaseCheckServiceError


def registering_exception_handlers(app: FastAPI):
    """
    Registering handlers for custom exceptions.
    """

    @app.exception_handler(BaseCheckServiceError)
    async def _exception(request: Request, exc: BaseCheckServiceError):

        return JSONResponse(
            status_code=422,
            content={
                "detail": exc.message,
                "extras": exc.extras,
            },
        )
