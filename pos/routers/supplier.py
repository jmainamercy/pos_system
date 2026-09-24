from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.schemas.supplier import SupplierCreate, SupplierRead, SupplierUpdate
from pos.services import supplier

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get(
    "/",
    response_model=list[SupplierRead],
)
def list_suppliers(db: Session = Depends(get_db)):
    return supplier.list_suppliers(db)


@router.get("/{id}", response_model=SupplierRead)
def get_supplier(id: int, db: Session = Depends(get_db)):
    return supplier.get_supplier(db, id)


@router.post("/", response_model=SupplierRead, status_code=status.HTTP_201_CREATED)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    return supplier.create_supplier(db, data)


@router.patch("/{id}", response_model=SupplierRead)
def update_supplier(id: int, data: SupplierUpdate, db: Session = Depends(get_db)):
    return supplier.update_supplier(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(id: int, db: Session = Depends(get_db)):
    supplier.delete_supplier(db, id)
