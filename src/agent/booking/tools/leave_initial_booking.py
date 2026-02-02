from typing import Annotated, Any

from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from agent.booking.enums import BookingEvent
from agent.booking.state import BookingState
from agent.common.helpers import tool_command
from api.enums import BookingDecision


@tool("leave_initial_booking")
def leave_initial_booking(
    state: Annotated[BookingState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command[Any]:
    """Keep the initial booking unchanged."""
    state.decision = BookingDecision.LEAVE_INITIAL
    state.last_event = BookingEvent.BOOKING_LEFT_INITIAL

    return tool_command(
        state=state,
        tool_call_id=tool_call_id,
        result=state.last_event,
    )
