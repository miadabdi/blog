"""
Generic repository for CRUD operations on SQLModel models.
"""

from typing import Any, Dict, Generic, Optional, Type, TypeVar

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..common.exceptions.exceptions import EntityNotFoundException
from .generic_model import GenericModel

T = TypeVar("T", bound=GenericModel)


class GenericRepository(Generic[T]):
    """
    Generic repository for CRUD operations.

    Args:
        model (Type[T]): The SQLModel model class.

    Methods:
        create, get_by_id, get_all, update, delete
    """

    def __init__(self, model: Type[T]):
        self.model = model

    async def _create_record(self, data: Dict[str, Any], session: AsyncSession) -> T:
        """
        Create a record without committing.

        Args:
            data (Dict[str, Any]): Data for the record.
            session (AsyncSession): Database session.

        Returns:
            T: The created record.
        """
        record = self.model(**data)

        session.add(record)
        await session.flush()  # Flush to get the ID and other DB-generated values
        await session.refresh(record)  # Refreshes with all DB-generated values

        return record

    async def create(self, data: Dict[str, Any], session: AsyncSession) -> T:
        """
        Create and commit a record.

        Args:
            data (Dict[str, Any]): Data for the record.
            session (AsyncSession): Database session.

        Returns:
            T: The created record.
        """
        record = await self._create_record(data, session)
        return record

    async def get_by_id(self, id: int, session: AsyncSession) -> Optional[T]:
        """
        Get a record by ID.

        Args:
            id (int): The record ID.
            session (AsyncSession): Database session.

        Returns:
            Optional[T]: The record if found, else None.
        """
        return (
            await session.exec(select(self.model).where(self.model.id == id))
        ).first()

    async def get_all(self, session: AsyncSession) -> list[T]:
        """
        Get all records.

        Args:
            session (AsyncSession): Database session.

        Returns:
            list[T]: List of all records.
        """
        return list((await session.exec(select(self.model))).all())

    async def update(self, id: int, data: Dict[str, Any], session: AsyncSession) -> T:
        """
        Update a record by ID.

        Args:
            id (int): The record ID.
            data (Dict[str, Any]): Data to update.
            session (AsyncSession): Database session.

        Returns:
            T: The updated record.

        Raises:
            EntityNotFoundException: If the record does not exist.
        """
        record = await self.get_by_id(id, session)
        if record is None:
            raise EntityNotFoundException(
                resource_id=str(id),
                resource=self.model.__name__,
            )

        record.sqlmodel_update(data)
        session.add(record)
        await session.flush()
        await session.refresh(record)
        return record

    async def delete(self, id: int, session: AsyncSession) -> T:
        """
        Delete a record by ID.

        Args:
            id (int): The record ID.
            session (AsyncSession): Database session.

        Returns:
            T: The deleted record.

        Raises:
            EntityNotFoundException: If the record does not exist.
        """
        record = await self.get_by_id(id, session)
        if record is None:
            raise EntityNotFoundException(
                resource_id=str(id),
                resource=self.model.__name__,
            )

        await session.delete(record)
        return record
