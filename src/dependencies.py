from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


# MARK: Session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    AsyncGenerator of an `AsyncSession` instance.

    Note:
    * The transaction would be automatically committed or rolled back
    in case of any exception at the exit from the context manager.
    * DB connection is checked out from the pool at first
    `AsyncSession.execute` call and remains so until the exit from the context manager.
    """

    async with SessionLocal.begin() as session:
        yield session
