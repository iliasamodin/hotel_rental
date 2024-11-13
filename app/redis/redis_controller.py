from typing import Callable

from fastapi import FastAPI
from fastapi_cache.decorator import cache
from starlette.routing import NoMatchFound
from httpx import Client
from icecream import ic

from app.settings import settings

from app.redis.deroctor_manager import RedisDeroctorManager


class RedisController:
    """
    Redis caching controller.
    """

    def __init__(
        self,
        redis_decorator_manager: RedisDeroctorManager = RedisDeroctorManager,
        client_maker: Client = Client,
    ):
        self.app: FastAPI | None = None
        self.warming_up_funcs: list[Callable] = list()
        self.redis_decorator_manager = redis_decorator_manager
        self.client_maker = client_maker

    def cache(
        self,
        warming_up=False,
        *args,
        **kwargs,
    ):
        """
        Determine whether function response needs to be cached.
        """

        if settings.CACHING and settings.MODE != "test":
            wrapper = cache(*args, **kwargs)

            if settings.NEED_TO_WARM_UP_CACHE and warming_up:
                wrapper = self.redis_decorator_manager.with_warming_up(
                    warming_up_funcs=self.warming_up_funcs,
                    wrapper=wrapper,
                )

        else:
            wrapper = self.redis_decorator_manager.without_caching(*args, **kwargs)

        return wrapper

    def warm_up_cache(self):
        """
        Warm up redis cache.

        :return: cache warm-up status.
        """

        if not isinstance(self.app, FastAPI):
            return False

        with self.client_maker() as client:
            for func in self.warming_up_funcs:
                try:
                    url = self.app.url_path_for(func.__name__)
                    client.get(
                        url=f"http://{settings.HOST}:{settings.PORT}{url}",
                    )

                except NoMatchFound:
                    ic(f"The function {func.__name__} is not a request handler.")

        return True


redis_controller = RedisController()
