from sqlalchemy.orm import Session
from pos.models.payment import Payment

class PaymentRepository:
    def __init__(self):
        self.model = Payment

    def get(self, db: Session, id: int) -> Payment | None:
        return db.get(self.model, id)

    def get_by_sale_id(self, db: Session, sale_id: int) -> list[Payment]:
        return db.query(self.model).filter(self.model.sale_id == sale_id).all()

    def create(self, db: Session, data: dict) -> Payment:
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

payment_repository = PaymentRepository()
