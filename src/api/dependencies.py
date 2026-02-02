from fastapi import Header, HTTPException, Request
from settings import settings
from starlette import status

from agent.booking.service import BookingService


def get_booking_svc(request: Request) -> BookingService:
    return request.app.state.booking_agent_service


async def verify_app_token(
    authorization: str | None = Header(None, alias="Authorization"),
) -> None:
    if authorization != settings.APP_AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )
