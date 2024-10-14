# from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    first_name: str
    last_name: str | None
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=6,
        description="Password must contain at least 6 characters"
    )


class UserRead(UserBase):
    id: int


class UserUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    username: str | None
    password: str | None = Field(
        None,
        min_length=6,
        description="Password must contain at least 6 characters"
    )

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str
