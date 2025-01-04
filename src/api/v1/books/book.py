from fastapi import APIRouter, Depends, HTTPException
from src.schema.books.book import BookBaseSchema, BookDetailSchema, BookUpdateSchema
from src.service.bookstore.books import book_service
from uuid import UUID
from functools import wraps

# def custom_exception_handler(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         try:
#             return await func(*args, **kwargs)
#         except HTTPException as e:
#
#             raise HTTPException(status_code=404, detail=f"Something Went Wrong see \n{e.detail}");
#         except Exception as e:
#             raise HTTPException(status_code= 500, detail = 'An unexpected error occurred')
#     return wrapper




book_api = APIRouter(prefix = '/book')

@book_api.post('/add', status_code = 201, response_model = BookDetailSchema)
# @custom_exception_handler
async def add_book(
        book: BookBaseSchema,
        service = Depends(book_service)
):
    book_to_be_added = await service.add(**book.dict())
    return book_to_be_added

@book_api.get('/detail/{id}', status_code = 200)
# @custom_exception_handler
async def book_detail(
        id: UUID,
        service = Depends(book_service)
):
    response = await service.get_by_id(id);
    return response



@book_api.patch('/update/{id}', status_code = 200, response_model = BookDetailSchema)
# @custom_exception_handler
async def update_book(
        id: UUID,
        book: BookUpdateSchema,
        service = Depends(book_service)
):

    response = await service.update(id, **book.dict(exclude_unset=True))
    return response

@book_api.delete('/soft_delete/{id}', status_code = 204)
# @custom_exception_handler
async def soft_delete(
        id: UUID,
        service = Depends(book_service)
):
    response = await service.soft_delete(id)
    return response

@book_api.delete('/hard_delete/{id}', status_code = 200)
# @custom_exception_handler
async def hard_delete(
        id: UUID,
        service = Depends(book_service)
):
    response = await service.hard_delete(id)
    if response != "Error":
        return {"detail":response}
    return {"detail": response}

@book_api.get('/rn_book', status_code = 200)
# @custom_exception_handler
async def rn_book():
    raise ValueError("SameThing")
