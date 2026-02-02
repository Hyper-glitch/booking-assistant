from langgraph.constants import END

from agent.booking.state import BookingState
from agent.common.decider import BaseDecider
from api.enums import BookingDecision


class Decider(BaseDecider):
    """
    Decides the next node in a dialogue graph based on the current user state.

    Used in LangGraph-style agent flows to route between stages like LLM processing,
    tool execution, or ending the conversation, depending on message history and logic phase.
    """

    @classmethod
    def entry(cls, state: BookingState) -> str:
        """Choose where to go after the “entry” node."""
        if state.decision == BookingDecision.TO_OPERATOR:
            return END

        return "llm"
