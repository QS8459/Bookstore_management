from typing import TypeVar, Generic, Type
from uuid import UUID
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.db.models.history.history import History
from sqlalchemy.future import select
from datetime import datetime
T = TypeVar('T')

class BaseService(ABC, Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def _execute_in_session(self, callback, operation_type: str, *args, **kwargs):
        async with self.session:
            try:
                if operation_type in ["write", "update"]:
                    result = await callback(*args, **kwargs)
                    await self.session.commit()
                    if result and operation_type != "update":
                        await self.session.refresh(result)
                    return result
                elif operation_type == 'read':
                    query = await callback(*args, **kwargs)
                    result = await self.session.execute(query)
                    if result:
                        return result.scalars().first()
            except IntegrityError as e:
                await self.session.rollback()
                raise ValueError("Database Integrity error occurred") from e
            except SQLAlchemyError as e:
                await self.session.rollback()
                raise RuntimeError("Database operation failed") from e

    @abstractmethod
    async def before_add(self, **kwargs):
        pass
    async def add(self, **kwargs) -> T:
        async def _create_instance(**kwargs):
            instance = self.model(**kwargs)
            await self.before_add(**kwargs)
            self.session.add(instance)
            return instance

        instance = await self._execute_in_session(_create_instance, 'write', **kwargs)
        field = BaseService.formatize(**kwargs)
        await self.add_history(md = History, model = self.model.__tablename__, action = "create", fields = field)

        return instance


    async def add_history(self, md: Type[T] , **kwargs):
        async def _create_instance(**kwargs):
            instance = md(**kwargs)

            self.session.add(instance)
            return instance

        instance = await self._execute_in_session(_create_instance, 'write', **kwargs )
        return instance

    async def _get_query_by_id(self, id:UUID):
        return select(self.model).where(self.model.id == id)

    async def get_by_id(self, id:UUID) -> T:
        query = self._get_query_by_id(id)
        instance = await self._execute_in_session(lambda:query,"read")
        return instance

    async def update(self, id: UUID, **kwargs) -> T:
        async def _update_instance(**kwargs):
            instance = await self.get_by_id(id)
            for k,v in kwargs.items():
                setattr(instance, k,v)
            return instance

        instance = await self._execute_in_session(_update_instance, "update",**kwargs)
        fields = BaseService.formatize(**kwargs)
        await self.add_history(History,model = self.model.__tablename__, action = "update", fields = fields)
        return instance

    @staticmethod
    def datetime_converter(o):
        if isinstance(o, datetime):
            return o.isoformat()
    @staticmethod
    def formatize(**kwargs):
        import json
        return json.dumps(kwargs, default=BaseService.datetime_converter)