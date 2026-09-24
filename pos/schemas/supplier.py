from pydantic import BaseModel, ConfigDict, Field


class SupplierBase(BaseModel):
    company_name: str = Field(..., max_length=150)
    contact_name: str | None = Field(None, max_length=100)
    phone: str = Field(..., max_length=20)
    email: str | None = Field(None, max_length=100)
    address: str | None = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    company_name: str | None = Field(None, max_length=150)
    contact_name: str | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=100)
    address: str | None = None


class SupplierRead(SupplierBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
