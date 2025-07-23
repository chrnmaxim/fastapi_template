import asyncio
from typing import AsyncGenerator

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import EngineLocal, SessionLocal

__all__ = ["faker"]

faker = Faker()


# MARK: DBSession
@pytest.fixture()
async def session() -> AsyncGenerator[AsyncSession, None]:
    """
    This connects the engine to Postgres, starts a transaction, then binds that connection
    to a session with a nested transaction. Nesting the transaction allows for the isolation
    mentioned above by allowing us to commit changes in the inner transaction so it’s only
    visible to the tests it is working with, but doesn’t fully commit data to the database as
    the outer transaction will never be committed.
    """

    async with EngineLocal.connect() as conn:
        tsx = await conn.begin()
        async with SessionLocal(bind=conn) as session:
            nested_tsx = await conn.begin_nested()

            yield session

            if nested_tsx.is_active:
                await nested_tsx.rollback()
            await tsx.rollback()


# MARK: Loop
@pytest.fixture(scope="session")
def event_loop(request):
    """
    The event_loop fixture is scoped to the entire testing session and allows Pytest
    to only have one active event loop for the entirety of the test run. The built-in
    event loop fixture with pytest-asyncio is function-scoped by default and using it
    will cause Pytest to error with lots of loop closed/open errors.
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
