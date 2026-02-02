import logging
from typing import Any, AsyncContextManager, Callable

from langchain_qwq import ChatQwen
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from agent.booking.context import BookingContext
from agent.booking.decider import Decider
from agent.booking.graph import BookingGraph
from agent.booking.prompts import BOOKING_PROMPT
from agent.booking.runner import BookingRunner
from agent.booking.service import BookingService
from agent.booking.state import BookingState
from agent.booking.tools import BOOKING_TOOLS
from integration.client import ExternalAPIClient
from settings import settings

logger = logging.getLogger(__name__)


def build_graph(
    checkpointer: BaseCheckpointSaver[Any],
) -> CompiledStateGraph[BookingState, BookingContext, BookingState, BookingState]:
    """Build graph for booking-assistant agent."""
    decider = Decider()
    graph = BookingGraph(
        decider=decider,
        checkpointer=checkpointer,
        tools=BOOKING_TOOLS,
        state_schema=BookingState,
        context_schema=BookingContext,
    ).build()

    return graph


def graph_builder(
    checkpointer: BaseCheckpointSaver[Any],
) -> CompiledStateGraph[BookingState, BookingContext, BookingState, BookingState]:
    """
    Wrapper for creating graph in the service layer.
    We need to make it because checkpointer can't work with pull db connections.
    """
    return build_graph(
        checkpointer=checkpointer,
    )


def create_booking_svc(
    chat_model: ChatQwen,
    api: ExternalAPIClient,
    saver_factory: Callable[[str], AsyncContextManager[BaseCheckpointSaver[str]]],
    dsn_provider: str,
) -> BookingService:
    logger.info("Starting to create booking service...")

    runner = BookingRunner(
        system_prompt=BOOKING_PROMPT,
        chat_model=chat_model,
        tools=BOOKING_TOOLS,
    )
    context = BookingContext(
        api=api,
        runner=runner,
    )
    svc = BookingService(
        graph_builder=graph_builder,
        saver_factory=saver_factory,
        dsn_provider=dsn_provider,
        context=context,
        recursion_limit=settings.GRAPH_RECURSION_LIMIT,
    )

    logger.info("Booking service created successfully.")
    return svc
