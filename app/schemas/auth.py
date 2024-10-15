from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
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


class Token(BaseModel):
    access_token: str
    token_type: str
