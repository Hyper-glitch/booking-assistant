from typing import Annotated, Any

from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.runtime import get_runtime
from langgraph.types import Command

from agent.booking.enums import BookingEvent
from agent.booking.state import BookingState
from agent.common.helpers import tool_command
from api.enums import BookingDecision
from integration.interface import ExternalAPIClient


@tool("keep_initial_booking")
async def keep_initial_booking(
    state: Annotated[BookingState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command[Any]:
    """Keep the initial booking unchanged."""
    api: ExternalAPIClient = get_runtime(BookingState).context.api

    response = await api.keep_initial_booking(booking_id=state.booking_id)
    if response.success:
        state.decision = BookingDecision.LEAVE_INITIAL
        state.last_event = BookingEvent.BOOKING_LEFT_INITIAL

    content = state.last_event if response.success else response.reason
    return tool_command(
        state=state,
        tool_call_id=tool_call_id,
        content=content,
    )
