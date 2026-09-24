from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.repository.sale import sale_repository
from pos.repository.sale_item import sale_item_repository


def list_items_by_sale(db: Session, sale_id: int):
    if not sale_repository.get(db, sale_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sale invoice with ID {sale_id} not found",
        )

    db_items = sale_item_repository.get_by_sale_id(db, sale_id)

    formatted_items = []
    for item in db_items:
        formatted_items.append(
            {
                "id": item.id,
                "sale_id": item.sale_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal,
                "product_name": item.product.name,
            }
        )

    return formatted_items
