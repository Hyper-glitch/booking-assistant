from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from agent.booking.state import BookingState
from api.enums import BookingDecision, Channel


class Meta(BaseModel):
    session_id: str
    channel: Channel = Channel.API


class AgentRequest(BaseModel):
    meta: Meta
    booking_id: str
    message: str

    def to_state(self) -> BookingState:
        return BookingState(
            session_id=self.meta.session_id,
            messages=[HumanMessage(content=self.message)],
            booking_id=self.booking_id,
        )


class AgentResponse(BaseModel):
    meta: Meta
    message: str
    decision: BookingDecision

    @classmethod
    def from_state(cls, state: BookingState, meta: Meta) -> "AgentResponse":
        """Build a response from the agent's state"""
        return cls(
            message=state.message[-1].content,
            decision=state.decision,
            meta=meta,
        )
