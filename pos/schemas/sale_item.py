from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be at least 1")


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemRead(SaleItemBase):
    id: int
    sale_id: int
    unit_price: Decimal = Field(..., max_digits=10, decimal_places=2)
    subtotal: Decimal = Field(..., max_digits=10, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)


class SaleItemExtendedRead(SaleItemRead):
    product_name: str = Field(
        ..., description="Pulled dynamically from product relationship"
    )
