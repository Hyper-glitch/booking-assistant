from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

from agent.booking.enums import BookingEvent
from agent.common.state import BaseState
from api.enums import BookingDecision
from integration.dto import Booking


class BookingState(BaseState):
    booking_id: str
    booking: Booking = None
    operator_requests: int = 0
    clarify_answer_attempts: int = 0
    decision: BookingDecision = BookingDecision.PENDING
    last_event: BookingEvent | None = None
    messages: Annotated[list[AnyMessage], add_messages]
