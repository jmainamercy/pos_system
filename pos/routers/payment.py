from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.schemas.payment import PaymentCreate, PaymentRead, PaymentSummary
from pos.services import payment as payment_service

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def collect_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
):
    return payment_service.process_payment(db, data)


@router.get("/sale/{sale_id}/status", response_model=PaymentSummary)
def check_sale_payment_status(
    sale_id: int,
    db: Session = Depends(get_db),
):
    return payment_service.get_payment_status(db, sale_id)
