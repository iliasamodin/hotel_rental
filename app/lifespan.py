from contextlib import asynccontextmanager
from typing import AsyncIterator, Coroutine

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from icecream import ic

from app.settings import settings

from app.db.session import async_engine, async_session_maker, sync_engine, sync_session_maker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Configuring the start and end of the application lifespan.
    """

    # Initializing a connection to redis
    redis = aioredis.from_url(url=settings.REDIS_URL)
    FastAPICache.init(
        backend=RedisBackend(redis=redis),
        prefix="cache",
    )

    try:
        yield

    finally:
        # Closing connections to external resources
        connection_killers = [
            async_session_maker.close_all,
            async_engine.dispose,
            sync_session_maker.close_all,
            sync_engine.dispose,
            redis.close,
        ]
        for connection_killer in connection_killers:
            try:
                call_result = connection_killer()
                if isinstance(call_result, Coroutine):
                    await call_result

            except Exception:
                ic(
                    f"Connection to external resource could not be closed. "
                    f"Call {connection_killer.__name__} failed."
                )
