from pydantic import BaseModel, ConfigDict, Field


class CustomerBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    phone_number: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=100)
    loyalty_points: int = Field(default=0, ge=0)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: str | None = Field(None, max_length=50)
    last_name: str | None = Field(None, max_length=50)
    phone_number: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=100)
    loyalty_points: int | None = Field(None, ge=0)


class CustomerRead(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
