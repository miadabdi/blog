from typing import Any, Dict, Generic, Optional, Type, TypeVar

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..common.exceptions.not_found import NotFoundException
from .generic_model import GenericModel

T = TypeVar("T", bound=GenericModel)


class GenericRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def _create_record(self, data: Dict[str, Any], session: AsyncSession) -> T:
        """Create a record without committing"""
        record = self.model(**data)

        session.add(record)
        await session.flush()  # Flush to get the ID and other DB-generated values
        await session.refresh(record)  # Refreshes with all DB-generated values

        return record

    async def create(self, data: Dict[str, Any], session: AsyncSession) -> T:
        """Create and commit a record"""
        record = await self._create_record(data, session)
        return record

    async def get_by_id(self, id: int, session: AsyncSession) -> Optional[T]:
        """Get a record by ID"""
        return (
            await session.exec(select(self.model).where(self.model.id == id))
        ).first()

    async def get_all(self, session: AsyncSession) -> list[T]:
        """Get all records"""
        return list((await session.exec(select(self.model))).all())

    async def update(self, id: int, data: Dict[str, Any], session: AsyncSession) -> T:
        """Update a record by ID"""
        record = await self.get_by_id(id, session)
        if record is None:
            raise NotFoundException(
                resource=self.model.__name__,
                resource_id=str(id),
            )

        record.sqlmodel_update(data)
        session.add(record)
        await session.flush()
        await session.refresh(record)
        return record

    async def delete(self, id: int, session: AsyncSession) -> T:
        """Delete a record by ID"""
        record = await self.get_by_id(id, session)
        if record is None:
            raise NotFoundException(
                resource=self.model.__name__,
                resource_id=str(id),
            )

        await session.delete(record)
        return record
