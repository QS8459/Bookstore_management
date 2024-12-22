from typing import TypeVar, Generic, Type
from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.db.models.history.history import History

T = TypeVar('T')

class BaseService(ABC, Generic[T]):

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def _execute_in_session(self, callback, *args, **kwargs):
        async with self.session:
            try:
                result = await callback(*args, **kwargs)
                await self.session.commit()
                await self.session.refresh(result)
                return result
            except SQLAlchemyError as e:
                await self.session.rollback()
                raise e


    async def add(self, **kwargs) -> T:
        async def _create_instance(**kwargs):
            instance = self.model(**kwargs)
            self.session.add(instance)
            return instance

        instance = await self._execute_in_session(_create_instance, **kwargs)
        # await self.session.refresh(instance)

        field = BaseService.formatize(**kwargs)
        await self.add_history(md = History, model = self.model.__tablename__, action = "create", fields = field)

        return instance

    async def add_history(self, md: Type[T] , **kwargs):
        async def _create_instance(**kwargs):
            instance = md(**kwargs)

            self.session.add(instance)
            return instance

        instance = await self._execute_in_session(_create_instance, **kwargs )
        # await self.session.refresh(instance)
        return instance

    @staticmethod
    def formatize(**kwargs):
        field_string:str = '{'
        for k,v in kwargs.items():
            field_string += f"\"{k}\": \"{v}\","
        field_string += "}"
        field_arr = [i for i in field_string]
        field_arr.pop(-2)
        result_string = ''.join(field_arr)
        return result_string
