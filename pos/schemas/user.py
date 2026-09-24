from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Alphanumeric usernames with symbols like dots or dashes",
    )
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(
        ..., max_length=20, description="Permissions level: admin, cashier, manager"
    )
    is_Active: bool


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        repr=False,
        description="Plain text password meeting safe strength standards",
    )


class UserUpdate(BaseModel):
    username: str | None = Field(
        None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$"
    )
    full_name: str | None = Field(None, min_length=2, max_length=100)
    role: str | None = Field(None, max_length=20)
    password: str | None = Field(None, min_length=8, max_length=128, repr=False)
    is_active: bool


class UserRead(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
