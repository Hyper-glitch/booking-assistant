from typing import Annotated, Any

from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.runtime import get_runtime
from langgraph.types import Command

from agent.booking.constants import MAX_OPERATOR_REQUESTS
from agent.booking.enums import BookingEvent
from agent.booking.state import BookingState
from agent.common.decorators.tool_loging import log_tool_execution
from agent.common.helpers import tool_command
from api.enums import BookingDecision
from integration.client import ExternalAPIClient


@tool("transfer_to_operator")
@log_tool_execution()
async def transfer_to_operator(
    state: Annotated[BookingState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command[Any]:
    """Mark booking to be handled by a human operator."""
    state.operator_requests += 1
    limit_reached = state.operator_requests > MAX_OPERATOR_REQUESTS
    if not limit_reached:
        state.last_event = BookingEvent.OPERATOR_REQUESTED
        return tool_command(state=state, tool_call_id=tool_call_id, content=state.last_event)

    api: ExternalAPIClient = get_runtime(BookingState).context.api
    state.decision = BookingDecision.TO_OPERATOR
    state.last_event = BookingEvent.OPERATOR_ESCALATED
    await api.transfer_to_operator(
        booking_id=state.booking_id,
        reason="User requested operator",
        context={"thread_id": state.thread_id},
    )
    return tool_command(state=state, tool_call_id=tool_call_id, content=state.last_event)
