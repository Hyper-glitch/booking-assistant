#!/usr/bin/env python3

"""
Interactive CLI for Booking Assistant Agent.
"""

import asyncio
import logging
from datetime import datetime, timezone
from uuid import uuid4

from langchain_qwq import ChatQwen
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agent.booking.builder import create_booking_svc
from api.schemas import AgentRequest
from integration.mocks import create_mock_external_api
from logger import setup_logger
from settings import settings

logger = logging.getLogger(__name__)


async def run_agent() -> None:
    booking_id = f"BK{datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:18]}"
    session_id = str(uuid4())

    api = create_mock_external_api(booking_id)
    chat_model = ChatQwen(**settings.llm_params, streaming=False, enable_thinking=False)
    service = create_booking_svc(
        chat_model=chat_model,
        api=api,
        saver_factory=AsyncPostgresSaver.from_conn_string,
        dsn_provider=settings.postgres_dsn,
    )

    logger.info("Starting booking assistant agent with mock API")
    logger.info("Type 'quit' to exit the conversation.\n")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            logger.info("Exiting agent interaction.")
            break

        raw_request = {
            "booking_id": booking_id,
            "meta": {"session_id": session_id},
            "message": user_input,
        }
        request = AgentRequest.model_validate(raw_request)

        try:
            agent_response = await service.invoke(state=request.to_state(), thread_id=session_id)
        except Exception as e:
            logger.error(f"Error during agent invocation: {e}")
            break
        else:
            agent_message = agent_response["messages"][-1].content
            logger.info(f"Agent: {agent_message}")


if __name__ == "__main__":
    setup_logger()
    asyncio.run(run_agent())
