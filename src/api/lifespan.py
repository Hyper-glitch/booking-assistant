from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from langchain_qwq import ChatQwen
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agent.booking.builder import create_booking_svc
from api.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    chat_model = ChatQwen(**settings.llm_params, streaming=False, enable_thinking=False)
    app.state.booking_agent_service = create_booking_svc(
        chat_model=chat_model,
        saver_factory=AsyncPostgresSaver.from_conn_string,
        dsn_provider=settings.dsn_provider,
    )
    yield
