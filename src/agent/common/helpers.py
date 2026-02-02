import importlib
import pkgutil
from typing import Any

from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool
from langgraph.types import Command
from langgraph.typing import StateT


def tool_command(
    *,
    state: StateT,
    tool_call_id: str,
    content: str,
) -> Command[Any]:
    """
    Create a LangGraph Command that persists tool results into agent state.

    Appends a ToolMessage to the message history and commits all state changes
    for the next graph step.
    """
    return Command(
        update={
            **state.model_dump(exclude={"messages"}),
            "messages": state.messages + [ToolMessage(content=content, tool_call_id=tool_call_id)],
        }
    )


def collect_tools(package_name: str) -> list[BaseTool]:
    tools: list[BaseTool] = []

    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        for obj in vars(module).values():
            if isinstance(obj, BaseTool):
                tools.append(obj)

    return tools
