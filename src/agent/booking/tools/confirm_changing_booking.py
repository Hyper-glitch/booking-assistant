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


@tool("confirm_changing_booking")
async def confirm_changing_booking(
    state: Annotated[BookingState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command[Any]:
    """Confirm that the booking should be changed."""
    api: ExternalAPIClient = get_runtime(BookingState).context.api

    response = await api.confirm_booking_change(
        booking_id=state.booking_id,
        window_id=state.selected_window_id,
    )
    if response.success:
        state.decision = BookingDecision.CONFIRM
        state.last_event = BookingEvent.BOOKING_CHANGE_CONFIRMED

    content = state.last_event if response.success else response.reason
    return tool_command(state=state, tool_call_id=tool_call_id, content=content)
