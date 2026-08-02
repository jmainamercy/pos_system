from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemRead(SaleItemBase):
    id: int
    sale_id: int
    unit_price: Decimal = Field(..., max_digits=10, decimal_places=2)
    subtotal: Decimal = Field(..., max_digits=10, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)

class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    discount: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=10, decimal_places=2)
    items: List[SaleItemCreate] = Field(..., min_length=1)

class SaleRead(BaseModel):
    id: int
    customer_id: Optional[int]
    user_id: int
    sale_date: datetime
    total_amount: Decimal
    discount: Decimal
    final_amount: Decimal
    items: List[SaleItemRead]

    model_config = ConfigDict(from_attributes=True)
