from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.models import Payment
from pos.repository.payment import payment_repository
from pos.repository.sale import sale_repository
from pos.schemas.payment import PaymentCreate


def get_payment_status(db: Session, sale_id: int):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale record not found"
        )

    existing_payments = payment_repository.get_by_sale_id(db, sale_id)
    total_paid = sum(Decimal(str(p.amount_paid)) for p in existing_payments)

    final_amount = Decimal(str(sale.final_amount))
    remaining_balance = final_amount - total_paid

    if total_paid >= final_amount:
        payment_status = "FULLY_PAID"
    elif total_paid > 0:
        payment_status = "PARTIALLY_PAID"
    else:
        payment_status = "UNPAID"

    return {
        "sale_id": sale_id,
        "final_amount": final_amount,
        "total_paid": total_paid,
        "remaining_balance": max(Decimal("0.00"), remaining_balance),
        "status": payment_status,
        "customer_id": sale.customer_id,
    }


def process_payment(db: Session, data: PaymentCreate) -> Payment:
    status_summary = get_payment_status(db, data.sale_id)
    remaining_owed = status_summary["remaining_balance"]

    if status_summary["status"] == "FULLY_PAID":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This sale invoice has already been settled in full",
        )

    if data.amount_paid > remaining_owed and data.payment_method != "Cash":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Overpayment rejected. Amount owed is {remaining_owed}, but received {data.amount_paid}",
        )

    payment_dict = data.model_dump()
    payment_dict["payment_date"] = datetime.now(timezone.utc)
    new_payment = payment_repository.create(db, payment_dict)

    updated_summary = get_payment_status(db, data.sale_id)
    if updated_summary["status"] == "FULLY_PAID" and updated_summary["customer_id"]:
        from pos.models.customer import Customer

        customer = db.get(Customer, updated_summary["customer_id"])
        if customer:
            earned_points = int(updated_summary["final_amount"] // 100)
            customer.loyalty_points += earned_points
            db.commit()

    return new_payment
