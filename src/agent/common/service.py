from typing import Any, AsyncContextManager, Callable

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.typing import ContextT, InputT, OutputT, StateT

from agent.common.decorators.handle_exceptions import handle_exceptions


class BaseAgentService:
    def __init__(
        self,
        context: Any,
        graph_builder: Callable[
            [BaseCheckpointSaver[str]], CompiledStateGraph[StateT, ContextT, InputT, OutputT]
        ],
        saver_factory: Callable[[str], AsyncContextManager[BaseCheckpointSaver[str]]],
        dsn_provider: str,
        **kwargs: Any,
    ) -> None:
        self._graph_builder = graph_builder
        self._saver_factory = saver_factory
        self._dsn_provider = dsn_provider
        self._context = context
        self._kwargs = kwargs

    @handle_exceptions()
    async def invoke(self, state: StateT, thread_id: str) -> StateT:
        config = RunnableConfig(configurable={"thread_id": thread_id}, **self._kwargs)
        async with self._saver_factory(self._dsn_provider) as saver:
            await saver.setup()  # type: ignore[attr-defined]
            graph: CompiledStateGraph[Any, Any, Any, Any] = self._graph_builder(saver)
            return await graph.ainvoke(state, config=config, context=self._context)
