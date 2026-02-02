from fastapi import Header, HTTPException, Request
from starlette import status

from agent.booking.service import BookingService
from settings import settings


def get_booking_svc(request: Request) -> BookingService:
    return request.app.state.booking_agent_service


async def verify_app_token(
    authorization: str | None = Header(None, alias="Authorization"),
) -> None:
    """Verify app token in each endpoint."""
    if authorization != settings.APP_AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )
