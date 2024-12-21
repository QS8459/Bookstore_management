from src.api.v1 import app
from fastapi import APIRouter

api = APIRouter(prefix = '/api')

api.include_router(app)