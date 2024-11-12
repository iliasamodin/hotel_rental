from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable

from fastapi.concurrency import run_in_threadpool


class RedisDeroctorManager:
    """
    Radis decorator manager.
    """

    @staticmethod
    def without_caching(*args, **kwargs):
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

    @staticmethod
    def with_warming_up(
        warming_up_funcs: list[Callable],
        wrapper: Callable,
    ):
        """
        Save decorator inner for later cache warm-up.
        """

        @wraps(wrapper)
        def substitute_wrapper(fucn: Callable):
            inner = wrapper(fucn)

            warming_up_funcs.append(inner)

            return inner

        return substitute_wrapper
