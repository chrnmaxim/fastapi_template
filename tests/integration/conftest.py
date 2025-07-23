from typing import AsyncGenerator

import httpx
import pytest_asyncio
from fastapi import APIRouter, FastAPI

from src.dependencies import get_session


# MARK: TestRouter
class BaseTestRouter:
    """Base class for testing routes."""

    router: APIRouter
    base_route: str

    @pytest_asyncio.fixture(scope="function")
    async def router_client(self, session) -> AsyncGenerator[httpx.AsyncClient, None]:
        """
        `AsyncGenerator` for `httpx.AsyncClient` instance.

        Configures `httpx.ASGITransport` to redirect all requests
        directly to the API using the ASGI protocol.
        """

        app = FastAPI()
        app.include_router(self.router)
        app.dependency_overrides[get_session] = lambda: session

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test"
        ) as async_client:
            yield async_client
