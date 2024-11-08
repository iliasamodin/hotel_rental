from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.settings import settings

from app.db.session import async_session_maker


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
        async_session_maker.close_all()
        await redis.close()
