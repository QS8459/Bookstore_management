from src.settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.db.models.base import Base
engine = create_async_engine(url = str(settings.pg_url))
async_session_maker = async_sessionmaker(engine, expire_on_commit = False)


async def get_async_session() -> None:
    async with async_session_maker() as session:
        yield session