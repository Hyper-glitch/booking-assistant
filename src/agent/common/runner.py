from abc import ABC, abstractmethod
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langgraph.typing import StateT


class BaseRunner(ABC):
    def __init__(
        self,
        system_prompt: str,
        chat_model: BaseChatModel,
        tools: Sequence[BaseTool],
    ) -> None:
        self.runnable = self._prepare_runnable(
            system_prompt=system_prompt, chat_model=chat_model, tools=tools
        )

    async def ainvoke(self, state: StateT) -> AIMessage:
        invoke_state = self.get_invoke_state(state)
        return await self.runnable.ainvoke(invoke_state)

    @abstractmethod
    def get_invoke_state(self, state: StateT) -> dict[str, Any]:
        """Must implement in child class."""

    @staticmethod
    def _prepare_runnable(system_prompt: str, chat_model: BaseChatModel, tools: Sequence[BaseTool]):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages", optional=True),
            ]
        )
        model = chat_model.bind_tools(tools, tool_choice="auto")
        runnable = prompt | model

        return runnable
