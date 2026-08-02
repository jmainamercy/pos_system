from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CustomerBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    loyalty_points: int = Field(default=0, ge=0)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    loyalty_points: Optional[int] = Field(None, ge=0)

class CustomerRead(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
