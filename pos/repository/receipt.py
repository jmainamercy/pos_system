from sqlalchemy.orm import Session, joinedload
from pos.models.receipt import Receipt

class ReceiptRepository:
    def __init__(self):
        self.model = Receipt

    def get(self, db: Session, id: int) -> Receipt | None:
        return db.query(self.model).options(
            joinedload(self.model.sale)
        ).filter(self.model.id == id).first()

    def get_by_sale_id(self, db: Session, sale_id: int) -> Receipt | None:
        return db.query(self.model).filter(self.model.sale_id == sale_id).first()

    def create(self, db: Session, data: dict) -> Receipt:
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

receipt_repository = ReceiptRepository()
