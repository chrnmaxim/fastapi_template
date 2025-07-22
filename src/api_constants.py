import os

from sqlalchemy import TextClause, text

# MARK: Security
ENV_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
CORS_METHODS = ("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT")

# MARK: Database
DB_NAMING_CONVENTION: dict[str, str] = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
POOL_RECYCLE: int = 3600
CURRENT_TIMESTAMP_UTC: TextClause = text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')")
DEFAULT_QUERY_OFFSET: int = 0
DEFAULT_QUERY_LIMIT: int = 100
