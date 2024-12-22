from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from src.settings import settings

engine: AsyncEngine = create_async_engine(url=str(settings.pg_url))
async_session_maker: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
