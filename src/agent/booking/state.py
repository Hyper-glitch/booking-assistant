from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

from agent.booking.enums import BookingEvent
from agent.common.state import BaseState
from api.enums import BookingDecision
from api.schemas import Meta


class BookingState(BaseState):
    meta: Meta
    operator_requests: int = 0
    clarify_answer_attempts: int = 0
    decision: BookingDecision
    last_event: BookingEvent | None = None
    messages: Annotated[list[AnyMessage], add_messages]
