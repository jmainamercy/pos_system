from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.models.user import User
from pos.repository.customer import customer_repository
from pos.repository.product import product_repository
from pos.repository.sale import sale_repository
from pos.schemas.sale import SaleCreate


def get_sale(db: Session, id: int):
    sale = sale_repository.get(db, id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale invoice record not found",
        )
    return sale


def list_sales(db: Session):
    return sale_repository.get_all(db)


def create_sale(db: Session, data: SaleCreate, current_user: User):
    if data.customer_id and not customer_repository.get(db, data.customer_id):
        raise HTTPException(
            status_code=400, detail="Invalid customer_id profile connection"
        )

    running_total = Decimal("0.00")
    items_to_save = []

    for item in data.items:
        product = product_repository.get(db, item.product_id)
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product ID {item.product_id} not found"
            )

        if product.stock_qty < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product '{product.name}'. In stock: {product.stock_qty}",
            )

        product.stock_qty -= item.quantity

        unit_price = Decimal(str(product.price))
        subtotal = unit_price * item.quantity
        running_total += subtotal

        items_to_save.append(
            {
                "product_id": product.id,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "subtotal": subtotal,
            }
        )

    final_amount = running_total - data.discount
    if final_amount < 0:
        final_amount = Decimal("0.00")

    sale_header = {
        "customer_id": data.customer_id,
        "user_id": current_user.id,
        "sale_date": datetime.now(timezone.utc),
        "total_amount": running_total,
        "discount": data.discount,
        "final_amount": final_amount,
    }

    sale_obj = sale_repository.create_sale_transaction(db, sale_header, items_to_save)
    # repository populates `saleitem` relationship; normalize to `items` for response model
    try:
        sale_obj.items = sale_obj.saleitem
    except AttributeError:
        pass
    return sale_obj
