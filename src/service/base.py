from typing import TypeVar, Generic, Type
from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
T = TypeVar('T')

class BaseService(ABC, Generic[T]):

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def add(self, **kwargs) -> T:
        try:
            async with self.session:
                instance = self.model(**kwargs)
                self.session.add(instance)
                await self.session.commit()
                await self.session.refresh(instance)
                return instance
        except SQLAlchemyError as e:
            raise e