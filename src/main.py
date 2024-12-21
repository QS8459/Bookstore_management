
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import api
from contextlib import asynccontextmanager
from src.settings import settings

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


engine: AsyncEngine
async_session_maker: async_sessionmaker
@asynccontextmanager
async def lifespan(_app: FastAPI):
    global engine, async_session_maker
    engine = create_async_engine(url=str(settings.pg_url))
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    yield
    await engine.dispose()

def init_routes(_app: FastAPI):
    app.include_router(api)

app = FastAPI(
    title = settings.app_title,
    description = settings.app_description,
    version = settings.app_version,
    lifespan = lifespan
)

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.on_event("shutdown")
async def shutdown():
    print("shutting down")
