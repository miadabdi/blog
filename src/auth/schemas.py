from pydantic import BaseModel, EmailStr, Field


class SignUp(BaseModel):
    email: EmailStr = Field()
    fname: str = Field(min_length=3)
    lname: str = Field(min_length=3)
    password: str = Field(min_length=8)


class UpdateUser(BaseModel):
    fname: str = Field(min_length=3)
    lname: str = Field(min_length=3)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    fname: str
    lname: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True  # Enable ORM mode to read data from SQLAlchemy models
