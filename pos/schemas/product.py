from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    category_id: int
    supplier_id: int
    barcode: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    cost_price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    stock_qty: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: int | None = None
    supplier_id: int | None = None
    barcode: str | None = Field(None, min_length=1, max_length=50)
    name: str | None = Field(None, min_length=1, max_length=150)
    price: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    cost_price: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    stock_qty: int | None = Field(None, ge=0)


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
