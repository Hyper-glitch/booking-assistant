"""Monitoring router for the Kubernetes API."""

from fastapi import APIRouter

router = APIRouter(
    prefix="/monitoring",
    include_in_schema=False,
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/status")
def liveness_probe() -> dict[str, bool]:
    """
    Liveness monitoring endpoint for Kubernetes.
    """
    return {"alive": True}


@router.get("/ready")
def readiness_probe() -> dict[str, bool]:
    """
    Readiness probe endpoint for Kubernetes.
    """
    return {"ready": True}
