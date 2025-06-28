from pydantic import BaseModel, Field

class CreatePost(BaseModel):
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    body: str = Field(min_length=1)
    featured_image: str = Field(min_length=1)

class UpdatePost(BaseModel):
    title: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    body: str | None = Field(default=None)
    featured_image: str | None = Field(default=None)
