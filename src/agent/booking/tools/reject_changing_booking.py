from typing import Annotated, Any

from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.runtime import get_runtime
from langgraph.types import Command

from agent.booking.enums import BookingEvent
from agent.booking.state import BookingState
from agent.common.helpers import tool_command
from api.enums import BookingDecision
from integration.client import ExternalAPIClient


@tool("reject_changing_booking")
async def reject_changing_booking(
    state: Annotated[BookingState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command[Any]:
    """Reject the proposed booking change."""
    api: ExternalAPIClient = get_runtime(BookingState).context.api
    response = await api.reject_booking_change(
        booking_id=state.booking_id,
        reason="User rejected the change.",
    )
    if response.success:
        state.decision = BookingDecision.REJECT
        state.last_event = BookingEvent.BOOKING_CHANGE_REJECTED

    content = state.last_event if response.success else response.reason
    return tool_command(
        state=state,
        tool_call_id=tool_call_id,
        content=content,
    )
