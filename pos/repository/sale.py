from sqlalchemy.orm import Session
from pos.models.sale import Sale
from pos.models.sale_item import SaleItem

class SaleRepository:
    def __init__(self):
        self.model = Sale

    def get(self, db: Session, id: int):
        return db.get(self.model, id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create_sale_transaction(self, db: Session, sale_data: dict, items_data: list):
        db_sale = self.model(**sale_data)
        db.add(db_sale)
        db.flush()
        for item in items_data:
            item["sale_id"] = db_sale.id
            db_item = SaleItem(**item)
            db.add(db_item)
            
        db.commit()
        db.refresh(db_sale)
        return db_sale

sale_repository = SaleRepository()
