from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from pos.services import customer

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=list[CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return customer.list_customers(db)


@router.get("/{id}", response_model=CustomerRead)
def get_customer(id: int, db: Session = Depends(get_db)):
    return customer.get_customer(db, id)


@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    return customer.create_customer(db, data)


@router.patch("/{id}", response_model=CustomerRead)
def update_customer(id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    return customer.update_customer(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id: int, db: Session = Depends(get_db)):
    customer.delete_customer(db, id)
