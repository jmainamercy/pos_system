import secrets
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.repository.receipt import receipt_repository
from pos.repository.sale import sale_repository
from pos.services.payment import get_payment_status


def generate_receipt_number() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    random_suffix = secrets.token_hex(3).upper()
    return f"REC-{today}-{random_suffix}"


def issue_receipt(db: Session, sale_id: int):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale invoice record missing"
        )

    existing_receipt = receipt_repository.get_by_sale_id(db, sale_id)
    if existing_receipt:
        return existing_receipt

    payment_summary = get_payment_status(db, sale_id)
    if payment_summary["status"] != "FULLY_PAID":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot issue receipt. Sale is {payment_summary['status']}. Owed: {payment_summary['remaining_balance']}",
        )

    receipt_dict = {
        "sale_id": sale_id,
        "receipt_number": generate_receipt_number(),
        "issued_at": datetime.now(timezone.utc),
    }

    return receipt_repository.create(db, receipt_dict)


def get_receipt(db: Session, id: int):
    receipt = receipt_repository.get(db, id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested receipt not found"
        )
    return receipt
