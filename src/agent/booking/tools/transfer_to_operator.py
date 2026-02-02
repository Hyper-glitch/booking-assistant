from typing import Annotated, Any

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from agent.booking.constants import MAX_OPERATOR_REQUESTS, TRANSFER_TO_OPERATOR_MSG, ASK_OPERATOR_REASON_MSG
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

    msg = TRANSFER_TO_OPERATOR_MSG if limit_reached else ASK_OPERATOR_REASON_MSG

    return tool_command(state=state, tool_call_id=tool_call_id, result=msg)
