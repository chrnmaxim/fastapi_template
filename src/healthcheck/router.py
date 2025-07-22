from fastapi import APIRouter, status

from src.healthcheck.schemas import HealthCheckSchema

__all__ = ["healthcheck_router"]

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["Check API status"])


@healthcheck_router.get(
    path="",
    summary="Check API status",
    response_model=None,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": HealthCheckSchema}},
)
async def healthcheck() -> HealthCheckSchema:
    """Check API status."""

    return HealthCheckSchema()
