import logging
from typing import Any

import aiohttp
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

from integration.dto import Booking, BookingChangeResponse, BookingWindow
from integration.interface import ExternalAPIInterface
from settings import settings

logger = logging.getLogger(__name__)


class ExternalAPIClient(ExternalAPIInterface):
    """HTTP client implementation for ExternalAPIClient."""

    def __init__(self, base_url: str, token: str):
        self._base_url = base_url
        self._token = token
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self._token}"}
            )
        return self._session

    @retry(
        stop=stop_after_attempt(settings.RETRY_STOP_AFTER_ATTEMPTS),
        wait=wait_fixed(settings.RETRY_WAIT_FIXED_SEC),
        retry=retry_if_exception_type(aiohttp.ClientError),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _get(self, path: str) -> dict[str, Any]:
        session = await self._get_session()
        async with session.get(f"{self._base_url}{path}") as resp:
            resp.raise_for_status()
            return await resp.json()

    @retry(
        stop=stop_after_attempt(settings.RETRY_STOP_AFTER_ATTEMPTS),
        wait=wait_fixed(settings.RETRY_WAIT_FIXED_SEC),
        retry=retry_if_exception_type(aiohttp.ClientError),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _post(self, path: str, json: dict) -> dict[str, Any]:
        session = await self._get_session()
        async with session.post(f"{self._base_url}{path}", json=json) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def get_booking(self, booking_id: str) -> Booking:
        data = await self._get(f"/bookings/{booking_id}")
        return Booking(**data)

    async def get_available_windows(self, booking_id: str) -> list[BookingWindow]:
        data = await self._get(f"/available_windows/{booking_id}")
        return [BookingWindow(**window) for window in data]

    async def confirm_booking_change(
        self, booking_id: str, window_id: str
    ) -> BookingChangeResponse:
        data = await self._post(f"/bookings/{booking_id}/confirm", {"window_id": window_id})
        return BookingChangeResponse(**data)

    async def keep_initial_booking(self, booking_id: str) -> BookingChangeResponse:
        data = await self._post(f"/bookings/{booking_id}/keep", {})
        return BookingChangeResponse(**data)

    async def reject_booking_change(
        self, booking_id: str, reason: str | None = None
    ) -> BookingChangeResponse:
        payload = {"reason": reason} if reason else {}
        data = await self._post(f"/bookings/{booking_id}/reject", payload)
        return BookingChangeResponse(**data)

    async def transfer_to_operator(self, booking_id: str, reason: str, context: dict) -> None:
        await self._post(
            f"/bookings/{booking_id}/transfer_to_operator", {"reason": reason, "context": context}
        )

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
