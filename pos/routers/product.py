from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from pos.schemas.product import ProductCreate, ProductRead, ProductUpdate
from pos.services import product as product_service

router = APIRouter(
    prefix="/products", tags=["products"], dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return product_service.list_products(db)


@router.get("/{id}", response_model=ProductRead)
def get_product(id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, id)


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, data)


@router.patch(
    "/{id}",
    response_model=ProductRead,
)
def update_product(id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    return product_service.update_product(db, id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(id: int, db: Session = Depends(get_db)):
    product_service.delete_product(db, id)
