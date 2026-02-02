from langchain_core.tools import BaseTool

from agent.common.helpers import collect_tools

BOOKING_TOOLS: list[BaseTool] = collect_tools("agent.booking.tools")
