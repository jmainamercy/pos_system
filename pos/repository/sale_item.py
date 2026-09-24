from sqlalchemy.orm import Session, joinedload

from pos.models.sale_item import SaleItem


class SaleItemRepository:
    def __init__(self):
        self.model = SaleItem

    def get(self, db: Session, id: int) -> SaleItem | None:
        return db.get(self.model, id)

    def get_by_sale_id(self, db: Session, sale_id: int) -> list[SaleItem]:
        return (
            db.query(self.model)
            .options(joinedload(self.model.product))
            .filter(self.model.sale_id == sale_id)
            .all()
        )

    def get_total_quantity_sold(self, db: Session, product_id: int) -> int:
        result = db.query(self.model).filter(self.model.product_id == product_id).all()
        return sum(item.quantity for item in result)


sale_item_repository = SaleItemRepository()
