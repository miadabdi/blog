from pydantic import BaseModel, EmailStr, Field


class SignUp(BaseModel):
    """
    Schema for user sign-up data.
    """

    email: EmailStr = Field()
    fname: str = Field(min_length=3)
    lname: str = Field(min_length=3)
    password: str = Field(min_length=8)


class UpdateUser(BaseModel):
    """
    Schema for updating user information.
    """

    fname: str = Field(min_length=3)
    lname: str = Field(min_length=3)


class Token(BaseModel):
    """
    Schema for authentication token response.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token payload data.
    """

    username: str


class UserPublic(BaseModel):
    """
    Public representation of a user (excluding sensitive fields).
    """

    id: int
    email: EmailStr
    fname: str
    lname: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
