from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    sale_id: int
    payment_method: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Payment method: Cash, Card, Mobile Money",
    )
    amount_paid: Decimal = Field(
        ...,
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Must be greater than zero",
    )


class PaymentRead(PaymentCreate):
    id: int
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentSummary(BaseModel):
    sale_id: int
    final_amount: Decimal
    total_paid: Decimal
    remaining_balance: Decimal
    status: str  # 'UNPAID', 'PARTIALLY_PAID', 'FULLY_PAID'
