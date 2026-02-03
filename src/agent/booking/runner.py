from langchain_core.messages import BaseMessage, trim_messages
from langchain_core.messages.utils import count_tokens_approximately

from agent.common.runner import BaseRunner


class BookingRunner(BaseRunner):
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
