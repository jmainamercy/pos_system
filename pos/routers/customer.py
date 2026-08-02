from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from pos.services import customer
from pos.schemas.customer import CustomerCreate, CustomerUpdate, CustomerRead
from pos.core.security import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=list[CustomerRead], dependencies=[Depends(get_current_user)])
def list_customers(db: Session = Depends(get_db)):
    return customer.list_customers(db)

@router.get("/{id}", response_model=CustomerRead, dependencies=[Depends(get_current_user)])
def get_customer(id: int, db: Session = Depends(get_db)):
    return customer.get_customer(db, id)

@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    return customer.create_customer(db, data)

@router.patch("/{id}", response_model=CustomerRead, dependencies=[Depends(get_current_user)])
def update_customer(id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    return customer.update_customer(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def delete_customer(id: int, db: Session = Depends(get_db)):
    customer.delete_customer(db, id)
