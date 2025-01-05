from typing import TypeVar, Generic, Type
from uuid import UUID
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.db.models.history.history import History
from sqlalchemy.future import select
from typing import Optional
T = TypeVar('T')

class BaseService(ABC, Generic[T]):

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def _execute_in_session(self, callback, refresh = False,*args, **kwargs):
        async with self.session:
            try:
                result = await callback(*args, **kwargs)
                await self.session.commit()
                if result and refresh:
                    await self.session.refresh(result)
                return result
            except IntegrityError as e:
                await self.session.rollback()
                raise ValueError("Database Integrity error occurred") from e
            except SQLAlchemyError as e:
                await self.session.rollback()
                raise RuntimeError("Database operation failed") from e


    async def _execute_read(self, query):
        async with self.session:
            try:
                instance = await self.session.execute(query)
                return instance.scalars().first()
            except SQLAlchemyError as e:
                await self.session.rollback()
                raise RuntimeError('Database operation failed') from e


    @abstractmethod
    def before_add(self, **kwargs):
        pass


    async def add(self, **kwargs) -> T:
        async def _create_instance(**kwargs):
            instance = self.model(**kwargs)
            self.before_add(**kwargs)
            self.session.add(instance)
            return instance

        instance = await self._execute_in_session(_create_instance, refresh = True, **kwargs)
        field = BaseService.formatize(**kwargs)
        await self.add_history(action = "create", fields = field)

        return instance


    async def add_history(self, action:str, fields:str):
        async def _create_instance():
            hist_instance = History(
                model = self.model.__tablename__,
                action = action,
                fields = fields
            )
            self.session.add(hist_instance)
            return hist_instance

        await self._execute_in_session(_create_instance)



    async def get_by_id(self, id:UUID) -> T:
        query = select(self.model).where(self.model.id == id)
        instance =  await self._execute_read(query)
        if not instance:
            return None
        return instance

    async def update(self, id: UUID, **kwargs) -> T:
        async def _update_instance(id,**kwargs):
            instance = await self.get_by_id(id)
            for k,v in kwargs.items():
                setattr(instance, k,v)
            self.session.add(instance)
            return instance

        instance = await self._execute_in_session(_update_instance,id=id,**kwargs)
        fields = BaseService.formatize(**kwargs)
        await self.add_history(action = "update", fields = fields)
        return instance

    async def soft_delete(self, id:UUID)-> Optional[dict]:
        async def _delete_softly(id:UUID):
            instance = await self.get_by_id(id = id)
            setattr(instance, 'is_active', False)
            self.session.add(instance)
            return instance

        await self._execute_in_session(_delete_softly, refresh = True,id= id)
        return {"detail":"Deleted Successfully"}

    async def hard_delete(self, id:UUID):
        async def _delete_hard(id:UUID):
            instance = await self.get_by_id(id = id)
            await self.session.delete(instance)
            return instance

        await self._execute_in_session(_delete_hard, id = id)
        check_var = await self.get_by_id(id)
        if check_var is None:
            return "Success"
        return "Error"

    async def filter(self, fields = None, **kwargs):
        """
        Filter records with dynamic criteria and select specific columns.

        Args:
            fields (list): List of fields to retrieve. If None, retrieves all columns.
                           Example: fields=["id", "name"]
            kwargs: Key-value pairs for filtering.
                    Example: filter(name="Alice", age=30)

        Returns:
            List of filtered results (as dictionaries if fields are specified) or None in case of error.
        """
        query = select(self.model)

        if fields:
            selected_fields = [getattr(self.model, field) for field in fields if hasattr(self.model, field)]
            if not selected_fields:
                raise AttributeError("No valid fields specified for selection.")
            query = select(*selected_fields)


        for field, value in kwargs.items():
            if hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
            else:
                raise AttributeError(f"Field '{field}' does not exist in model '{self.model.__name__}'.")

        response = await self._execute_read(query)

        if not response:
            return None
        return response


    @staticmethod
    def formatize(**kwargs):
        import json
        return json.dumps(kwargs, default=str)