import time
from http import HTTPStatus
from typing import Callable

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator
from settings import settings


class APIRequestMetrics:
    _labelnames = ("method", "endpoint", "http_status")

    def __init__(self) -> None:
        self.request_count = Counter(
            name="api_requests_total",
            documentation="Total number of API requests",
            labelnames=self._labelnames,
        )

        self.request_latency = Histogram(
            name="api_request_latency_seconds",
            documentation="API request latency",
            labelnames=self._labelnames,
        )

        self.request_errors = Counter(
            name="api_request_errors_total",
            documentation="Total number of API error responses (4xx, 5xx)",
            labelnames=self._labelnames,
        )

        self.request_exceptions = Counter(
            name="api_request_exceptions_total",
            documentation="Unhandled exceptions during request processing",
            labelnames=("method", "endpoint", "exception_type"),
        )

    async def middleware(self, request: Request, call_next: Callable) -> Response:
        method = request.method
        route = request.scope.get("route")
        endpoint = route.path if route else "unknown"

        start_time = time.perf_counter()
        try:
            response: Response = await call_next(request)
        except Exception as exc:
            self.request_exceptions.labels(
                method,
                endpoint,
                type(exc).__name__,
            ).inc()
            raise

        latency = time.perf_counter() - start_time
        status_code = str(response.status_code)

        self.request_count.labels(method, endpoint, status_code).inc()
        self.request_latency.labels(method, endpoint, status_code).observe(latency)

        if response.status_code >= HTTPStatus.BAD_REQUEST:
            self.request_errors.labels(method, endpoint, status_code).inc()

        return response


def setup_metrics(app: FastAPI) -> None:
    instrumentator = Instrumentator(
        excluded_handlers=[
            "/monitoring/.*",
            "/metrics",
            "/docs",
            "/openapi.json",
            "/$",
        ]
    )

    instrumentator.instrument(app).expose(
        app,
        include_in_schema=False,
        endpoint=settings.METRICS_URL,
    )
