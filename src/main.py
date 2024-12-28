from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, ResponseValidationError
from src.api import api
from contextlib import asynccontextmanager
from src.settings import settings
from src.configuration import engine





@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()

def init_routes(_app: FastAPI):
    app.include_router(api)

app = FastAPI(
    title = settings.app_title,
    description = settings.app_description,
    version = settings.app_version,
    lifespan = lifespan,
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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "detail": exc.detail
        }
    )

@app.exception_handler(ResponseValidationError)
async def validation_error_handler(request: Request, exc):
    return JSONResponse(
        status_code = 418,
        content = {
            "message": f"{exc.body}, something went wrong"
        }
    )
