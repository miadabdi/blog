from sqlmodel import Field, SQLModel


class PostCategoryLink(SQLModel, table=True):
    post_id: int = Field(foreign_key="posts.id", primary_key=True)
    category_id: int = Field(foreign_key="categories.id", primary_key=True)


class PostTagLink(SQLModel, table=True):
    post_id: int = Field(foreign_key="posts.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
