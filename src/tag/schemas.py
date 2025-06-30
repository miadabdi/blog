from pydantic import BaseModel, Field


class CreateTag(BaseModel):
    name: str = Field(min_length=1)


class UpdateTag(BaseModel):
    name: str | None = None


class TagPublic(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True
