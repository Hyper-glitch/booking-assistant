"""
Tool execution logger for LangGraph agents.
"""

import functools
import logging
import time
from typing import Any, Callable, Coroutine

from settings import settings

logger = logging.getLogger(__name__)


def log_tool_execution() -> Callable:
    """
    Decorator for structured logging of LangGraph tool executions.
    """

    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable:
        func_name = func.__name__

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            state = kwargs.get("state") or (args[0] if args else None)
            tool_call_id = kwargs.get("tool_call_id") or (args[1] if len(args) > 1 else "unknown")

            context = {
                "tool_name": func_name,
                "tool_call_id": tool_call_id,
            }

            for attr in ("booking_id", "thread_id", "session_id", "user_id"):
                if hasattr(state, attr):
                    context[attr] = getattr(state, attr)

            logger.log(
                settings.LOG_LEVEL,
                "TOOL START | name=%s | call_id=%s%s",
                func_name,
                tool_call_id,
                "".join(
                    f" | {k}={v}"
                    for k, v in context.items()
                    if k not in ("tool_name", "tool_call_id")
                ),
                extra={**context, "stage": "start"},
            )

            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                logger.log(
                    settings.LOG_LEVEL,
                    "TOOL END   | name=%s | call_id=%s | duration=%.3fs | success=True",
                    func_name,
                    tool_call_id,
                    duration,
                    extra={
                        **context,
                        "stage": "end",
                        "duration_sec": round(duration, 3),
                        "success": True,
                    },
                )
                return result

            except Exception as exc:
                duration = time.perf_counter() - start_time
                logger.exception(
                    "TOOL ERROR | name=%s | call_id=%s | duration=%.3fs | error=%s",
                    func_name,
                    tool_call_id,
                    duration,
                    exc.__class__.__name__,
                    extra={
                        **context,
                        "stage": "error",
                        "duration_sec": round(duration, 3),
                        "success": False,
                        "error_type": exc.__class__.__name__,
                    },
                )
                raise

        return wrapper

    return decorator
