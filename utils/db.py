from asyncio import current_task

# from config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import scoped_session, sessionmaker

from utils.config import settings

db_url = (
    f"postgresql+asyncpg://"
    f"{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_DB}"
)

engine = create_async_engine(
    db_url,
    encoding="utf-8",
    # echo=settings.get("DATABASE_ECHO_MODE", False),
    max_overflow=settings.get("DB_CONN_MAX_OVERFLOW", 25),
)


# Dependency
async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session
