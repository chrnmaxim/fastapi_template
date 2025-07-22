from typing import Literal

from pydantic import BaseModel, Field

from src.api_config import api_settings


class HealthCheckSchema(BaseModel):
    """Schema for API status response."""

    mode: Literal["PROD", "DEV", "LOCAL", "TEST"] = Field(
        default=api_settings.MODE, description="API Mode"
    )
    version: str = Field(
        default=api_settings.APP_VERSION,
        description="API version. Corresponds to the latest commit hash",
    )
    status: str = Field(default="OK", description="API status")
