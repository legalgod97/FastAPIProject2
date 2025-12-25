import asyncio
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")

async def retry_async(
    func: Callable[[], Awaitable[T]],
    *,
    attempts: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 5.0,
    retry_exceptions: tuple[type[Exception], ...],
) -> T:
    last_exc: Exception | None = None

    for attempt in range(attempts):
        try:
            return await func()

        except retry_exceptions as exc:
            last_exc = exc

            if attempt == attempts - 1:
                break

            delay = min(base_delay * (2 ** attempt), max_delay)
            delay = random.uniform(0, delay)  # jitter

            await asyncio.sleep(delay)

    raise last_exc