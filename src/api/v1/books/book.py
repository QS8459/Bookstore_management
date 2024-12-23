from fastapi import APIRouter, Depends
from src.schema.books.book import BookBaseSchema, BookDetailSchema, BookUpdateSchema
from src.service.bookstore.books import book_service
from uuid import UUID
book_api = APIRouter(prefix = '/book')

@book_api.post('/add', status_code = 201, response_model = BookDetailSchema)
async def add_book(
        books: BookBaseSchema,
        service = Depends(book_service)
):
    try:
        a = await service.add(**books.dict())
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


# @book_api.patch('/update', status_code = 200, response_model = BookDetailSchema)
# async def update_book(
#         book: BookUpdateSchema,
#         service = Depends(book_service)
# ):
#     try:
#         response = await service.update(**book.dict())
#         return response
#     except Exception as e:
#         raise e