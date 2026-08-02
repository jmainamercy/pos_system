from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

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
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    barcode: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    price: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    cost_price: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    stock_qty: Optional[int] = Field(None, ge=0)

class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
