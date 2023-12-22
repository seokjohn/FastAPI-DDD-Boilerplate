from typing import TypeVar, Type, Optional, Generic, Any

from sqlalchemy import func, select, update, delete

from core.db.session import Base, session
from core.repository.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)
ModelIdType = TypeVar("ModelIdType", bound=Any)


class CRUDRepository(Generic[ModelType, ModelIdType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.attr_names = self.model.__table__.columns.keys()

    async def total(self, **parms):
        filter = [
            getattr(self.model, key) == value
            for key, value in parms.items()
        ]
        query = select(func.count()).where(*filter)
        result = await session.execute(query)
        return result.scalar()

    async def all_by_filter(self, **params):
        query = select(self.model).filter_by(**params)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: ModelIdType) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_by_filter(self, **params) -> Optional[ModelType]:
        query = select(self.model).filter_by(**params)
        result = await session.execute(query)
        return result.scalars().first()

    async def update_by_id(
            self,
            id: ModelIdType,
            params: dict,
            synchronize_session: SynchronizeSessionEnum = SynchronizeSessionEnum.FALSE,
    ) -> None:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**params)
            .execution_options(synchronize_session=synchronize_session.value)
        )
        await session.execute(query)

    async def update_by_filter(
            self,
            filter_params: dict,
            value_params: dict,
            synchronize_session: SynchronizeSessionEnum =  SynchronizeSessionEnum.FETCH,
    ) -> None:
        filter = [
            getattr(self.model, key) == value
            for key, value in filter_params.items()
        ]
        query = (
            update(self.model)
            .where(*filter)
            .values(**value_params)
            .execution_options(synchronize_session=synchronize_session.value)
        )
        await session.execute(query)

    async def delete(self, model: ModelType) -> None:
        await session.delete(model)

    async def delete_by_id(
            self,
            id: ModelIdType,
            synchronize_session: SynchronizeSessionEnum = SynchronizeSessionEnum.FETCH,
    ) -> None:
        query = (
            delete(self.model)
            .where(self.model.id == id)
            .execution_options(synchronize_session=synchronize_session.value)
        )
        await session.execute(query)

    async def delete_by_filter(
            self,
            filter_params: dict,
            synchronize_session: SynchronizeSessionEnum = SynchronizeSessionEnum.FETCH,
    ) -> None:
        filter = [
            getattr(self.model, key) == value
            for key, value in filter_params.items()
        ]
        query = (
            delete(self.model)
            .where(*filter)
            .execution_options(synchronize_session=synchronize_session.value)
        )
        await session.execute(query)

    async def save(self, model: ModelType) -> ModelType:
        session.add(model)
        await session.flush()
        await session.refresh(model)
        return model