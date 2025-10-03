from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from src.api_config import api_settings
from src.healthcheck.schemas import HealthCheckSchema

__all__ = ["healthcheck_router"]

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["Check API status"])


@healthcheck_router.get(
    path="",
    summary="Check API status",
    responses={status.HTTP_200_OK: {"model": HealthCheckSchema}},
)
async def healthcheck() -> ORJSONResponse:
    """Check API status."""

    return ORJSONResponse(
        content={
            "mode": api_settings.MODE,
            "version": api_settings.APP_VERSION,
            "status": "OK",
        },
        status_code=status.HTTP_200_OK,
    )
