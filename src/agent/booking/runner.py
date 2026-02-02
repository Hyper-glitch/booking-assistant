from typing import Any

from langchain_core.messages import BaseMessage, trim_messages
from langchain_core.messages.utils import count_tokens_approximately

from agent.booking.state import BookingState
from agent.common.runner import BaseRunner
from api.settings import settings


class BookingRunner(BaseRunner):
    def get_invoke_state(self, state: BookingState, **kwargs: Any) -> dict[str, Any]:
        messages = self._preprocess(state.messages, settings.LLM_TRIM_MESSAGES_MAX_TOKENS)
        return {
            "messages": messages,
            **kwargs,
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
