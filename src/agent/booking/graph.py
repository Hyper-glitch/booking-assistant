from typing import Any

from langgraph.runtime import get_runtime

from agent.booking.context import BookingContext
from agent.booking.state import BookingState
from agent.common.graph import BaseGraph


class BookingGraph(BaseGraph[BookingState, BookingContext, BookingState, BookingState]):

    async def _entry_node(self, state: BookingState) -> dict[str, Any]:
        """Get booking info by booking_id."""
        api = get_runtime(BookingContext).context.api
        booking = await api.get_booking_info(state.booking_id)
        return {"booking": booking}
