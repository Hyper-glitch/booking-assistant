from typing import Any

from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langgraph.typing import StateT


def tool_command(
    *,
    state: StateT,
    tool_call_id: str,
    result: str,
) -> Command[Any]:
    """
    Create a LangGraph Command that persists tool results into agent state.

    Appends a ToolMessage to the message history and commits all state changes
    for the next graph step.
    """
    return Command(
        update={
            **state.model_dump(exclude={"messages"}),
            "messages": state.messages + [ToolMessage(content=result, tool_call_id=tool_call_id)],
        }
    )
