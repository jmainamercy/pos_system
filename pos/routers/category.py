from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from pos.services import category
from pos.schemas.category import CategoryCreate, CategoryUpdate, CategoryRead
from pos.core.security import get_current_user, RoleChecker

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[CategoryRead], dependencies=[Depends(get_current_user)])
def list_categories(db: Session = Depends(get_db)):
    return category.list_categories(db)

@router.get("/{id}", response_model=CategoryRead, dependencies=[Depends(get_current_user)])
def get_category(id: int, db: Session = Depends(get_db)):
    return category.get_category(db, id)

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(["admin", "manager"]))])
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    return category.create_category(db, data)

@router.patch("/{id}", response_model=CategoryRead, dependencies=[Depends(RoleChecker(["admin", "manager"]))])
def update_category(id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    return category.update_category(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RoleChecker(["admin", "manager"]))])
def delete_category(id: int, db: Session = Depends(get_db)):
    category.delete_category(db, id)
