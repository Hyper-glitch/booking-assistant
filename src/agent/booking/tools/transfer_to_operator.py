from typing import Annotated, Any

from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from agent.booking.constants import MAX_OPERATOR_REQUESTS
from agent.booking.enums import BookingEvent
from agent.booking.state import BookingState
from agent.common.helpers import tool_command
from api.enums import BookingDecision


@tool("transfer_to_operator")
def transfer_to_operator(
    state: Annotated[BookingState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command[Any]:
    """Mark booking to be handled by a human operator."""
    state.operator_requests += 1
    limit_reached = state.operator_requests > MAX_OPERATOR_REQUESTS

    if limit_reached:
        state.decision = BookingDecision.TO_OPERATOR
        state.last_event = BookingEvent.OPERATOR_ESCALATED
    else:
        state.last_event = BookingEvent.OPERATOR_REQUESTED

    return tool_command(
        state=state,
        tool_call_id=tool_call_id,
        result=state.last_event,
    )
