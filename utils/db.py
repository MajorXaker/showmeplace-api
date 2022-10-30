# from config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from utils.config import settings

pure_db_url = (
    f"{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_DB}"
)
async_db_url = f"postgresql+asyncpg://{pure_db_url}"
db_url = f"postgresql://{pure_db_url}"

async_engine = create_async_engine(
    async_db_url,
    encoding="utf-8",
    echo=settings.get("DATABASE_ECHO_MODE", False),
    max_overflow=settings.get("DB_CONN_MAX_OVERFLOW", 25),
)


# Dependency
async def get_session() -> AsyncSession:
    async with AsyncSession(async_engine) as session:
        yield session
