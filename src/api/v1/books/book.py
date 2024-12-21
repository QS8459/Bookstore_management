from fastapi import APIRouter, Depends
from src.schema.books.book import BookBaseSchema, BookDetail
from src.service.bookstore.books import book_service
book_api = APIRouter(prefix = '/book')

@book_api.post('/add', status_code = 201, response_model = BookDetail)
async def add_book(
        books: BookBaseSchema,
        service = Depends(book_service)
):
    try:
        a = await service.add(**books.dict())
        return a
    except Exception as e:
        raise e