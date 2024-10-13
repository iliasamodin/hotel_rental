from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable

from fastapi.concurrency import run_in_threadpool
from fastapi_cache.decorator import cache

from app.settings import settings


class RedisController:
    """
    Redis caching controller.
    """

    def without_caching(self, *args, **kwargs):
        """
        Execute function without caching.
        """

        def wrapper(func: Callable):
            @wraps(func)
            async def inner(*args, **kwargs):
                if iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return await run_in_threadpool(
                        func=func,
                        *args,
                        **kwargs,
                    )

            return inner

        return wrapper

    def cache(self, *args, **kwargs):
        """
        Determine whether function response needs to be cached.
        """

        if settings.CACHING and settings.MODE != "test":
            return cache(*args, **kwargs)

        return self.without_caching(*args, **kwargs)


redis_controller = RedisController()
