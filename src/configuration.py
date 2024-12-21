#
# from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
# from contextlib import asynccontextmanager
# from src.settings import settings
# from src.main import app
# engine: AsyncEngine
# async_session_maker: async_sessionmaker
#
#
# @asynccontextmanager
# async def lifespan(app):
#     global engine, async_session_maker
#     engine = create_async_engine(url=str(settings.pg_url))
#     async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
#     yield
#     await engine.dispose()
