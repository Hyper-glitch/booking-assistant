from typing import Annotated, Any

from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from agent.booking.enums import BookingEvent
from agent.booking.state import BookingState
from agent.common.helpers import tool_command
from api.enums import BookingDecision


@tool("confirm_changing_booking")
def confirm_changing_booking(
    state: Annotated[BookingState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command[Any]:
    """Confirm that the booking should be changed."""
    state.decision = BookingDecision.CONFIRM
    state.last_event = BookingEvent.BOOKING_CHANGE_CONFIRMED
    return tool_command(state=state, tool_call_id=tool_call_id, result=state.last_event)
