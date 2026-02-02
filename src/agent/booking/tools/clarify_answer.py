from typing import Annotated, Any

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from agent.booking.constants import MAX_CLARIFY_ANSWER_ATTEMPTS, TRANSFER_TO_OPERATOR_MSG, CLARIFY_ANSWER
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
    limit_reached = state.clarify_answer_attempts >= MAX_CLARIFY_ANSWER_ATTEMPTS

    if limit_reached:
        state.decision = BookingDecision.TO_OPERATOR

    msg = TRANSFER_TO_OPERATOR_MSG if limit_reached else CLARIFY_ANSWER

    return tool_command(
        state=state,
        tool_call_id=tool_call_id,
        result=msg,
    )
