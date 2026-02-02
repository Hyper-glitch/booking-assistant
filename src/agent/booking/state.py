from datetime import datetime
from typing import Annotated, Any

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel

from agent.booking.enums import BookingEvent
from agent.common.state import BaseState
from api.enums import BookingDecision
from api.schemas import Meta


class BookingWindow(BaseModel):
    window_start_date_time: datetime | None = None
    window_end_date_time: datetime | None = None


class Booking(BaseModel):
    address: dict[str, Any]
    total_sla: int
    delivery_window: BookingWindow


class BookingState(BaseState):
    meta: Meta
    operator_requests: int = 0
    clarify_answer_attempts: int = 0
    decision: BookingDecision
    last_event: BookingEvent | None = None
    messages: Annotated[list[AnyMessage], add_messages]
