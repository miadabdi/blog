from pydantic import BaseModel, Field


class CreateCategory(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None


class UpdateCategory(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryPublic(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None

    class Config:
        from_attributes = True
