import httpx
from fastapi import status

from src.api_config import api_settings
from src.healthcheck.router import healthcheck_router
from src.healthcheck.schemas import HealthCheckSchema
from tests.integration.conftest import BaseTestRouter


class TestHealthcheckRouter(BaseTestRouter):
    """Class fot testing src.healthcheck.router.healthcheck_router."""

    router = healthcheck_router
    base_route = healthcheck_router.prefix

    # MARK: Get
    async def test_healthcheck(self, router_client: httpx.AsyncClient):
        """Can successfully check the API status."""

        response = await router_client.get(url=self.base_route)
        assert response.status_code == status.HTTP_200_OK

        healthcheck_data = HealthCheckSchema(**response.json())
        assert healthcheck_data.mode == api_settings.MODE
        assert healthcheck_data.version == api_settings.APP_VERSION
        assert healthcheck_data.status == "OK"
