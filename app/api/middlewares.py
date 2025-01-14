from fastapi import FastAPI, Request, Response
from time import perf_counter
from loguru import logger

from app.settings import settings


def registering_middlewares(app: FastAPI):
    """
    Registering middlewares.
    """

    @app.middleware("http")
    async def log_slow_requests(request: Request, call_next) -> Response:
        """
        Log execution time of slow requests.
        """

        start_time = perf_counter()

        response = await call_next(request)

        process_time = perf_counter() - start_time

        if process_time >= settings.CUTOFF_OF_SLOW_REQUESTS:
            logger.info(
                f"Slow request processing: {request.method} {request.url.path}, process time: {process_time} seconds.",
            )

        return response
