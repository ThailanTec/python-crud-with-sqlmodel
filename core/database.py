from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from core.configs import settigns

engine: AsyncEngine = create_async_engine(settigns.DB_URL)

Session: AsyncSession = sessionmaker(
    autoflush= False,
    autocommit= False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)