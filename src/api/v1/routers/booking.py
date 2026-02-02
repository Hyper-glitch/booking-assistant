import logging

from fastapi import APIRouter, Depends, Security

from agent.booking.service import BookingService
from api.dependencies import get_booking_svc, verify_app_token
from api.schemas import AgentRequest, AgentResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/booking-agent/invoke")
async def invoke(
    request: AgentRequest,
    service: BookingService = Depends(get_booking_svc),
    _: None = Security(verify_app_token),
) -> AgentResponse:
    """Endpoint for invoke booking agent."""
    logger.info("Request body:\n%s", request.model_dump_json(indent=4))

    state = await service.invoke(state=request)
    response = AgentResponse.from_state(state=state, meta=request.meta)

    logger.info("Response body:\n%s", response.model_dump_json(indent=4))
    return response
