from fastapi import APIRouter, Depends
from src.schema.books.book import BookBaseSchema, BookDetailSchema, BookUpdateSchema
from src.service.bookstore.books import book_service
from uuid import UUID
book_api = APIRouter(prefix = '/book')

@book_api.post('/add', status_code = 201, response_model = BookDetailSchema)
async def add_book(
        book: BookBaseSchema,
        service = Depends(book_service)
):
    try:
        a = await service.add(**book.dict())
        return a
    except Exception as e:
        raise e

@book_api.get('/detail/{id}', status_code = 200)
async def book_detail(
        id: UUID,
        service = Depends(book_service)
):
    try:
        response = await service.get_by_id(id);
        return response
    except Exception as e:
        raise e;


@book_api.patch('/update/{id}', status_code = 200, response_model = BookDetailSchema)
async def update_book(
        id: UUID,
        book: BookUpdateSchema,
        service = Depends(book_service)
):
    try:
        response = await service.update(id, **book.dict(exclude_unset=True))
        return response
    except Exception as e:
        raise e