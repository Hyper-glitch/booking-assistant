from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncGenerator

from fastapi import FastAPI
from langchain_qwq import ChatQwen
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agent.booking.builder import create_booking_svc
from api.metrics import APIRequestMetrics, setup_metrics
from api.v1.routers.booking import router as agent_router
from api.v1.routers.monitoring import router as monitoring_router
from integration.client import ExternalAPIClient
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    chat_model = ChatQwen(**settings.llm_params, streaming=False, enable_thinking=False)
    api = ExternalAPIClient(
        base_url=settings.EXTERNAL_API_URL,
        token=settings.EXTERNAL_API_TOKEN,
    )
    app.state.booking_agent_service = create_booking_svc(
        chat_model=chat_model,
        api=api,
        saver_factory=AsyncPostgresSaver.from_conn_string,
        dsn_provider=settings.postgres_dsn,
    )
    yield
    await api.close()


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


app = create_app(lifespan)
