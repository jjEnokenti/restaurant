from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.configs.config import BaseConfig

__all__ = (
    'db',
    'SessionLocal'
)

db = create_async_engine(
    BaseConfig.SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True
)

SessionLocal = AsyncSession(
    bind=db,
    expire_on_commit=False
)
