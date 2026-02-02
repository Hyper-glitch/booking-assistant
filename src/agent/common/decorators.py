import logging
from functools import wraps
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar

logger = logging.getLogger(__name__)


P = ParamSpec("P")
S = TypeVar("S")


def handle_exceptions(
    on_exception: (
        Callable[[Exception, tuple[Any, ...], dict[str, Any]], Awaitable[S]] | None
    ) = None,
    log: bool = True,
) -> Callable[[Callable[P, Awaitable[S]]], Callable[P, Awaitable[S]]]:  # noqa: WPS231
    """
    Universal decorator to handle exceptions in service layer.
    """

    def decorator(func: Callable[P, Awaitable[S]]) -> Callable[P, Awaitable[S]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> S:
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                if log:
                    logger.exception(
                        f"Error while running agent. Exception in {func.__name__}: {exc}"
                    )
                if on_exception is not None:
                    return await on_exception(exc, args, kwargs)

                raise exc

        return wrapper

    return decorator
