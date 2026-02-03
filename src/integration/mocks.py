import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from unittest.mock import AsyncMock

from mimesis import Address, Datetime, Person
from mimesis.locales import Locale

from integration.dto import Booking, BookingChangeResponse, BookingWindow

logger = logging.getLogger(__name__)


def generate_mock_booking(booking_id: str | None = None) -> Booking:
    """Generate a mock booking with realistic data using mimesis."""
    person = Person(Locale.EN)
    address = Address(Locale.EN)
    datetime_gen = Datetime(Locale.EN)

    if not booking_id:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        booking_id = f"BK{timestamp[:18]}"

    address_line = address.address()
    city = address.city()
    state = address.state()
    zip_code = address.postal_code()
    full_address = f"{address_line}, {city}, {state} {zip_code}"

    hotel_names = [
        "Grand Plaza Hotel",
        "City Center Inn",
        "Sunset Resort",
        "Mountain View Lodge",
        "Ocean Breeze Hotel",
        "Urban Escape Hotel",
        "Harbor View Inn",
        "Riverside Suites",
        "The Royal Palm",
        "Parkview Hotel",
        "Seaside Retreat",
        "Downtown Grand",
    ]
    hotel_name = person.random.choice(hotel_names)

    floor = person.random.randint(1, 20)
    room_on_floor = person.random.randint(1, 30)
    room_letter = person.random.choice(["", "A", "B", "C"])
    room_number = f"{floor}{room_on_floor:02d}{room_letter}"

    start_time = datetime_gen.datetime(start=2024, end=2026).replace(tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=2)

    total_sla = 60 + person.random.randint(0, 99)

    statuses = ["confirmed", "pending", "cancelled", "completed", "in-progress"]
    status = person.random.choice(statuses)

    return Booking(
        booking_id=booking_id,
        address=full_address,
        hotel_name=hotel_name,
        room_number=room_number,
        window=BookingWindow(start_date_time=start_time, end_date_time=end_time),
        total_sla=total_sla,
        status=status,
    )


def generate_mock_available_windows(count: int = 3) -> list[BookingWindow]:
    """Generate mock available booking windows using mimesis."""
    datetime_gen = Datetime(Locale.EN)
    windows = []

    for _ in range(count):
        start_time = datetime_gen.datetime(start=2026, end=2026).replace(tzinfo=timezone.utc)
        end_time = start_time + timedelta(hours=2)
        windows.append(BookingWindow(start_date_time=start_time, end_date_time=end_time))

    logger.info(f"mock_available_windows: {windows}")
    return windows


def generate_mock_booking_change_response(
    success: bool = True, reason: Optional[str] = None, updated_booking: Optional[Booking] = None
) -> BookingChangeResponse:
    """Generate a mock booking change response using mimesis."""
    person = Person(Locale.EN)

    if reason is None:
        reasons = [
            "Booking change rejected due to system constraints",
            "Customer requested to keep original booking",
            "No available windows for the requested date",
            "Booking change requires manual approval",
            "System error occurred during processing",
        ]
        reason = person.random.choice(reasons)

    if updated_booking is None:
        updated_booking = generate_mock_booking()

    return BookingChangeResponse(success=success, reason=reason, updated_booking=updated_booking)


def create_mock_external_api(booking_id: str) -> AsyncMock:
    """Create a fully mocked ExternalAPIClient with all methods pre-configured using mimesis."""
    mock_client = AsyncMock()

    mock_client.get_booking = AsyncMock(return_value=generate_mock_booking(booking_id))
    mock_client.get_available_windows = AsyncMock(return_value=generate_mock_available_windows())
    mock_client.confirm_booking_change = AsyncMock(
        return_value=generate_mock_booking_change_response(
            success=True, updated_booking=generate_mock_booking(booking_id="BK123456-CHANGED")
        )
    )
    mock_client.keep_initial_booking = AsyncMock(
        return_value=generate_mock_booking_change_response(
            success=True, reason="Initial booking kept as requested"
        )
    )

    mock_client.reject_booking_change = AsyncMock(
        return_value=generate_mock_booking_change_response(
            success=False, reason="Booking change rejected by system"
        )
    )
    mock_client.transfer_to_operator = AsyncMock(return_value=None)

    return mock_client
