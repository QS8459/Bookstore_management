from src.api.v1.books.book import book_api
from src.api.v1.users.users import users_api
from fastapi import APIRouter

app = APIRouter(prefix='/v1')
app.include_router(book_api)
app.include_router(users_api)

