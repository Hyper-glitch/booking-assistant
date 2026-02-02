from collections.abc import Callable
from typing import Any, AsyncContextManager

from fastapi import FastAPI

from api.metrics import APIRequestMetrics, setup_metrics
from api.settings import settings
from api.v1.routers.booking import router as agent_router
from api.v1.routers.monitoring import router as monitoring_router


def create_app(lifespan: Callable[[FastAPI], AsyncContextManager[Any]]) -> FastAPI:
    """
    Create and configure an instance of the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="REST API AI Agent Booking Assistant",
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    setup_metrics(app)
    app.middleware("http")(APIRequestMetrics().middleware)

    app.include_router(router=monitoring_router)
    app.include_router(prefix="/api/v1", router=agent_router)

    return app


app = create_app(settings)
