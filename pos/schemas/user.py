from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=50, 
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Alphanumeric usernames with symbols like dots or dashes"
    )
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(..., max_length=20, description="Permissions level: admin, cashier, manager")

class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=128, 
        repr=False,
        description="Plain text password meeting safe strength standards"
    )

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$")
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=8, max_length=128, repr=False)

class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
