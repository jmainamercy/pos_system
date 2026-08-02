from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class SupplierBase(BaseModel):
    company_name: str = Field(..., max_length=150)
    contact_name: Optional[str] = Field(None, max_length=100)
    phone: str = Field(..., max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    company_name: Optional[str] = Field(None, max_length=150)
    contact_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None

class SupplierRead(SupplierBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
