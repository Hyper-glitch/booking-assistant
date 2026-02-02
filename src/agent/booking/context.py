from dataclasses import dataclass

from agent.booking.runner import BookingRunner
from integration.client import ExternalAPIClient


@dataclass
class BookingContext:
    """
    Static context: Immutable data that doesn't change during execution (API, db connections, etc)
    https://langchain-ai.github.io/langgraph/agents/context/
    """

    api: ExternalAPIClient
    runner: BookingRunner
