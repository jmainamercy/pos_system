from sqlalchemy.orm import Session
from pos.models.product import Product

class ProductRepository:
    def __init__(self):
        self.model = Product

    def get(self, db: Session, id: int) -> Product | None:
        return db.get(self.model, id)

    def get_all(self, db: Session) -> list[Product]:
        return db.query(self.model).all()

    def create(self, db: Session, data: dict) -> Product:
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Product, data: dict) -> Product:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Product) -> None:
        db.delete(db_obj)
        db.commit()

product_repository = ProductRepository()
