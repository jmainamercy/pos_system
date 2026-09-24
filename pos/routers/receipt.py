from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.schemas.receipt import ReceiptFullExport, ReceiptRead
from pos.services import receipt as receipt_service

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.post(
    "/sale/{sale_id}", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED
)
def generate_sale_receipt(
    sale_id: int,
    db: Session = Depends(get_db),
):
    return receipt_service.issue_receipt(db, sale_id)


@router.get("/{id}", response_model=ReceiptFullExport)
def get_receipt_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    return receipt_service.get_receipt(db, id)
