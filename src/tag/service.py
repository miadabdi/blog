from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from ..common.exceptions.exceptions import (
    DuplicateEntryException,
    EntityNotFoundException,
    InternalException,
)
from .models import Tag
from .repository import TagRepository, get_TagRepository
from .schemas import CreateTag, UpdateTag


class TagService:
    def __init__(self, repo: TagRepository):
        self.repository = repo

    async def create_tag(self, data: CreateTag, session: AsyncSession) -> Tag:
        try:
            tag_record = await self.repository.create(data.model_dump(), session)
        except IntegrityError:
            raise DuplicateEntryException(
                resource=Tag.__name__, field="name", value=data.name
            )
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while creating the category.",
                underlying_error=e,
            )
        return tag_record

    async def update_tag(
        self, id: int, update_data: UpdateTag, session: AsyncSession
    ) -> Tag:
        tag_data = update_data.model_dump(exclude_unset=True)
        try:
            updated_tag = await self.repository.update(id, tag_data, session)
        except IntegrityError:
            raise DuplicateEntryException(
                resource=Tag.__name__, field="name", value=update_data.name
            )
        except Exception as e:
            raise InternalException(
                message="An unexpected error occurred while creating the category.",
                underlying_error=e,
            )

        return updated_tag

    async def delete_tag(self, id: int, session: AsyncSession) -> Tag:
        result = await self.repository.delete(id, session)
        return result

    async def get_tag_by_id(self, id: int, session: AsyncSession) -> Tag:
        result = await self.repository.get_by_id(id, session)
        if result is None:
            raise EntityNotFoundException(Tag.__name__, str(id))
        return result

    async def get_all_tags(self, session: AsyncSession) -> list[Tag]:
        return await self.repository.get_all(session)


@lru_cache
def get_TagService(
    tagRepository: Annotated[TagRepository, Depends(get_TagRepository)],
) -> TagService:
    return TagService(tagRepository)
