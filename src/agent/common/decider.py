from typing import Any, cast

from langgraph.prebuilt import tools_condition
from langgraph.typing import StateT


class BaseDecider:
    """
    Base decider for decision-making logic in a dialogue flow.
    """

    @classmethod
    def entry(cls, state: StateT) -> str:
        """Choose where to go after the “entry” node."""
        return "llm"

    @classmethod
    def llm(cls, state: StateT) -> str:
        """Decide where to go after the LLM node. Defaults to tools_condition.
        You can override this method to change the default behavior."""
        return tools_condition(cast(Any, state))

    @classmethod
    def tools(cls, state: StateT) -> str:
        """Decide where to go after the action (tool call) node."""
        return "llm"
