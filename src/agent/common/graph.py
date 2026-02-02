from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Sequence

from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.constants import END
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.runtime import get_runtime
from langgraph.typing import ContextT, InputT, OutputT, StateT

from agent.common.decider import BaseDecider
from agent.common.runner import BaseRunner


class BaseGraph(ABC, Generic[StateT, ContextT, InputT, OutputT]):
    def __init__(
        self,
        decider: BaseDecider,
        checkpointer: BaseCheckpointSaver[Any],
        tools: Sequence[BaseTool | Callable[..., Any]],
        state_schema: type[StateT],
        context_schema: type[ContextT] | None = None,
    ) -> None:
        self._decider = decider
        self._checkpointer = checkpointer
        self._tools = tools
        self._state_schema = state_schema
        self._context_schema = context_schema

    def build(self) -> CompiledStateGraph[StateT, ContextT, InputT, OutputT]:
        graph = StateGraph(state_schema=self._state_schema, context_schema=self._context_schema)

        graph.add_node("entry", self._entry_node)
        graph.add_node("llm", self._llm_node)
        graph.add_node("tools", ToolNode(self._tools))

        graph.set_entry_point("entry")

        graph.add_conditional_edges(
            "entry",
            self._decider.entry,
            {
                END: END,
                "llm": "llm",
            },
        )
        graph.add_conditional_edges(
            "llm",
            self._decider.llm,
            {
                "tools": "tools",
                "__end__": END,
            },
        )
        graph.add_conditional_edges(
            "tools",
            self._decider.tools,
            {
                END: END,
                "llm": "llm",
            },
        )

        return graph.compile(checkpointer=self._checkpointer)  # type: ignore[return-value]

    @abstractmethod
    async def _entry_node(self, state: StateT) -> dict[Any, Any]:
        """Subclasses must implement the graph construction logic."""

    async def _llm_node(self, state: StateT) -> dict[str, AIMessage]:
        ctx = get_runtime(self._context_schema).context
        chat_result = await ctx.runner.ainvoke(state)
        return {"messages": chat_result}
