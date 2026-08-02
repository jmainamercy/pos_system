from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class ReceiptUserSummary(BaseModel):
    full_name: str
    model_config = ConfigDict(from_attributes=True)

class ReceiptItemDetail(BaseModel):
    product_name: str = Field(..., alias="name", validation_alias="product") 
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    
    @classmethod
    def model_validate(cls, obj, **kwargs):
        return cls(
            product_name=obj.product.name,
            quantity=obj.quantity,
            unit_price=obj.unit_price,
            subtotal=obj.subtotal
        )

class ReceiptPaymentDetail(BaseModel):
    payment_method: str
    amount_paid: Decimal
    model_config = ConfigDict(from_attributes=True)

class ReceiptSaleSnapshot(BaseModel):
    sale_date: datetime
    total_amount: Decimal
    discount: Decimal
    final_amount: Decimal
    user: ReceiptUserSummary
    items: List[ReceiptItemDetail]
    payments: List[ReceiptPaymentDetail]
    model_config = ConfigDict(from_attributes=True)

class ReceiptBase(BaseModel):
    sale_id: int
    receipt_number: str
    issued_at: datetime

class ReceiptRead(ReceiptBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ReceiptFullExport(ReceiptRead):
    sale: ReceiptSaleSnapshot
