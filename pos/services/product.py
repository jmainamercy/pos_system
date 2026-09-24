from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.models.category import Category
from pos.models.product import Product
from pos.models.supplier import Supplier
from pos.repository.product import product_repository
from pos.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, id: int) -> Product:
    product = product_repository.get(db, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found"
        )
    return product


def list_products(db: Session) -> list[Product]:
    return product_repository.get_all(db)


def create_product(db: Session, data: ProductCreate) -> Product:
    if not db.get(Category, data.category_id):
        raise HTTPException(
            status_code=400, detail="Invalid category_id: Category does not exist"
        )
    if not db.get(Supplier, data.supplier_id):
        raise HTTPException(
            status_code=400, detail="Invalid supplier_id: Supplier does not exist"
        )

    return product_repository.create(db, data.model_dump())


def update_product(db: Session, id: int, data: ProductUpdate) -> Product:
    product_obj = get_product(db, id)
    update_data = data.model_dump(exclude_unset=True)
    if "category_id" in update_data and not db.get(
        Category, update_data["category_id"]
    ):
        raise HTTPException(
            status_code=400, detail="Invalid category_id mapping target"
        )
    if "supplier_id" in update_data and not db.get(
        Supplier, update_data["supplier_id"]
    ):
        raise HTTPException(
            status_code=400, detail="Invalid supplier_id mapping target"
        )

    return product_repository.update(db, product_obj, update_data)


def delete_product(db: Session, id: int) -> None:
    product_obj = get_product(db, id)
    product_repository.delete(db, product_obj)
