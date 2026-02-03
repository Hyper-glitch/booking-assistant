from typing import Any
from aiocache import cached
from langgraph.runtime import get_runtime

from agent.booking.context import BookingContext
from agent.booking.state import BookingState
from agent.common.graph import BaseGraph
from integration.client import ExternalAPIClient


class BookingGraph(BaseGraph[BookingState, BookingContext, BookingState, BookingState]):

    @cached(
        ttl=300,
        key_builder=lambda func, *args, **kwargs: f"booking:{args[0]}"
    )
    async def _entry_node(self, state: BookingState) -> dict[str, Any]:
        """Get booking info by booking_id."""
        api: ExternalAPIClient = get_runtime(BookingContext).context.api
        booking = await api.get_booking(state.booking_id)
        return {"booking": booking.model_dump(mode="json")}
