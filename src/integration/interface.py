from abc import ABC, abstractmethod

from integration.dto import Booking, BookingChangeResponse, BookingWindow


class ExternalAPIInterface(ABC):
    """Abstract client for external booking system."""

    @abstractmethod
    async def get_booking(self, booking_id: str) -> Booking:
        """Return current booking details."""

    @abstractmethod
    async def get_available_windows(self, booking_id: str) -> list[BookingWindow]:
        """Return alternative booking windows."""

    @abstractmethod
    async def confirm_booking_change(
        self, booking_id: str, window_id: str
    ) -> BookingChangeResponse:
        """Confirm booking change to selected booking window."""

    @abstractmethod
    async def keep_initial_booking(self, booking_id: str) -> BookingChangeResponse:
        """Explicitly keep the original booking."""

    @abstractmethod
    async def reject_booking_change(
        self, booking_id: str, reason: str | None = None
    ) -> BookingChangeResponse:
        """Reject booking change."""

    @abstractmethod
    async def transfer_to_operator(self, booking_id: str, reason: str, context: dict) -> None:
        """Transfer booking handling to a human operator."""
