from typing import Any

from langchain_core.messages import BaseMessage, trim_messages
from langchain_core.messages.utils import count_tokens_approximately

from agent.booking.state import BookingState
from agent.common.runner import BaseRunner
from settings import settings


class BookingRunner(BaseRunner):
    def get_invoke_state(self, state: BookingState) -> dict[str, Any]:
        """Prepare information that injects in system prompt."""
        messages = self._preprocess(state.messages, settings.LLM_TRIM_MESSAGES_MAX_TOKENS)
        return {
            "messages": messages,
            "booking_id": state.booking.booking_id,
            "hotel_name": state.booking.hotel_name,
            "address": state.booking.address,
            "room_number": state.booking.room_number,
            "window": state.booking.window,
            "status": state.booking.status,
        }

    @staticmethod
    def _preprocess(messages: list[BaseMessage], max_tokens: int) -> list[BaseMessage]:
        messages = trim_messages(
            messages,
            max_tokens=max_tokens,
            token_counter=count_tokens_approximately,
            start_on="human",
            end_on=("human", "tool"),
            include_system=False,
        )
        return messages
