from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


# MARK: Session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    AsyncGenerator of an `AsyncSession` instance.

    Note:
    * The session would rollback automatically inside
    the context manager in case of exception at closure.
    * Connection is checkout from the pool at first call to the session.
    * Commit must be done explicitly.
    """

    async with SessionLocal() as session:
        try:
            yield session
        except Exception as ex:
            raise ex
