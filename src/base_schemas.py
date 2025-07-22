from pydantic import BaseModel, Field

from src import api_constants


class BaseQuerySchema(BaseModel):
    """Base query params schema for pagination."""

    offset: int | None = Field(
        default=api_constants.DEFAULT_QUERY_OFFSET, description="Query offset"
    )
    limit: int | None = Field(
        default=api_constants.DEFAULT_QUERY_LIMIT, description="Query limit"
    )
    asc: bool = Field(default=True, description="Sorting order on a selected field")


class BaseListReadSchema(BaseModel):
    """Base schema for read data in list."""

    count: int = Field(description="Total count of the results matching query params")
