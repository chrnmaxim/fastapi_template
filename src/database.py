from sqlalchemy import AsyncAdaptedQueuePool, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src import api_constants
from src.api_config import api_settings

__all__ = ["Base", "EngineLocal", "SessionLocal"]


class Base(DeclarativeBase):
    """
    Base class for all database models.
    Inherits from sqlalchemy.orm.DeclarativeBase.
    """

    metadata = MetaData(naming_convention=api_constants.DB_NAMING_CONVENTION)


EngineLocal = create_async_engine(
    url=api_settings.DATABASE_URL,
    pool_size=api_settings.POOL_SIZE,
    max_overflow=api_settings.MAX_OVERFLOW,
    poolclass=AsyncAdaptedQueuePool,
    pool_pre_ping=False,
    pool_recycle=api_constants.POOL_RECYCLE,
    echo=True if api_settings.MODE == "LOCAL" else False,
    connect_args={
        "server_settings": {
            "application_name": f"{api_settings.APP_NAME}_{api_settings.MODE}"
        }
    },
)

SessionLocal = async_sessionmaker(
    bind=EngineLocal,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)
