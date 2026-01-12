import asyncio
import random
from collections.abc import Callable, Awaitable
from typing import TypeVar, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")


def retry_async(
    *,
    attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 5.0,
    retry_exceptions: tuple[type[Exception], ...],
):
    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exc: Exception | None = None

            for attempt in range(attempts):
                try:
                    return await func(*args, **kwargs)

                except retry_exceptions as exc:
                    last_exc = exc

                    if attempt == attempts - 1:
                        break

                    delay = min(base_delay * (2 ** attempt), max_delay)
                    delay = random.uniform(0, delay)  # jitter
                    await asyncio.sleep(delay)

            raise last_exc

        return wrapper

    return decorator