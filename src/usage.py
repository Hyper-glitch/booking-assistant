#!/usr/bin/env python3

"""
Interactive CLI for Booking Assistant Agent.
"""

import asyncio
import logging
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

from langchain_core.messages import HumanMessage
from langchain_qwq import ChatQwen
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agent.booking.builder import create_booking_svc
from agent.booking.state import BookingState
from api.schemas import AgentRequest
from integration.mocks import create_mock_external_api
from logger import setup_logger
from settings import settings

logger = logging.getLogger(__name__)


def prepare_agent_state(
    existing_state: BookingState | None,
    user_message: str,
    request: AgentRequest,
) -> BookingState:
    if existing_state is not None:
        state = deepcopy(existing_state)
        state["messages"] += [HumanMessage(content=user_message)]
    else:
        state = request.to_state()

    return state


async def run_agent() -> None:
    booking_id = f"BK{datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:18]}"
    session_id = str(uuid4())
    updated_state = None

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

        request = AgentRequest.model_validate(
            {
                "booking_id": booking_id,
                "meta": {"session_id": session_id},
                "message": user_input,
            }
        )
        state = prepare_agent_state(
            existing_state=updated_state, user_message=user_input, request=request
        )

        try:
            updated_state = await service.invoke(state=state, thread_id=session_id)
        except Exception as exc:
            logger.error(f"Error during agent invocation: {exc}")
            break
        else:
            agent_message = updated_state["messages"][-1].content
            logger.info(f"Agent: {agent_message}")


if __name__ == "__main__":
    setup_logger()
    asyncio.run(run_agent())
