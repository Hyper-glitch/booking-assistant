from typing import Annotated, Any

from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from agent.booking.constants import MAX_CLARIFY_ANSWER_ATTEMPTS
from agent.booking.enums import BookingEvent
from agent.booking.state import BookingState
from agent.common.helpers import tool_command
from api.enums import BookingDecision


@tool("clarify_answer")
def clarify_answer(
    state: Annotated[BookingState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command[Any]:
    """
    Clarify the user's answer or transfer to an operator if max attempts reached.
    """
    state.clarify_answer_attempts += 1
    limit_reached = state.clarify_answer_attempts > MAX_CLARIFY_ANSWER_ATTEMPTS

    if limit_reached:
        state.decision = BookingDecision.TO_OPERATOR
        state.last_event = BookingEvent.CLARIFY_LIMIT_REACHED
    else:
        state.last_event = BookingEvent.CLARIFY_REQUESTED

    return tool_command(state=state, tool_call_id=tool_call_id, result=state.last_event)
