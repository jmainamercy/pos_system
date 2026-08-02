from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from pos.services import sale
from pos.schemas.sale import SaleCreate, SaleRead
from pos.core.security import get_current_user, RoleChecker
from pos.models.user import User

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/", response_model=list[SaleRead], dependencies=[Depends(RoleChecker(["admin", "manager"]))])
def list_sales(db: Session = Depends(get_db)):
    return sale.list_sales(db)

@router.get("/{id}", response_model=SaleRead, dependencies=[Depends(get_current_user)])
def get_sale(id: int, db: Session = Depends(get_db)):
    return sale.get_sale(db, id)

@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(data: SaleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return sale.create_sale(db, data, current_user)
