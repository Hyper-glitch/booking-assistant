from typing import Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langgraph.typing import StateT


class BaseRunner:
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
        return await self.runnable.ainvoke(state)

    @staticmethod
    def _prepare_runnable(system_prompt: str, chat_model: BaseChatModel, tools: Sequence[BaseTool]):
        prompt = ChatPromptTemplate.from_messages(
            [
                (SystemMessage.type, system_prompt),
                MessagesPlaceholder(variable_name="messages", optional=True),
            ]
        )
        model = chat_model.bind_tools(tools, tool_choice="auto")
        runnable = prompt | model

        return runnable
