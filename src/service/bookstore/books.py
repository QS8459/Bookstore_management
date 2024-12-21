from src.service.base import BaseService
from src.db.engine import get_async_session
from fastapi import Depends
from src.db.models.units.books import Books
from sqlalchemy.ext.asyncio import AsyncSession


class BookService(BaseService):
    def __init__(self, session):
        super().__init__(session, Books)


def book_service(session: AsyncSession = Depends(get_async_session)) -> AsyncSession:

    return BookService(session)