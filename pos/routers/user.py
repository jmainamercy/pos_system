from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from pos.services import user
from pos.schemas.user import UserCreate, UserUpdate, UserRead
from pos.core.security import RoleChecker

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return user.list_users(db)

@router.get("/{id}", response_model=UserRead)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(db, id)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(["admin"]))])
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return user.create_user(db, data)

@router.patch("/{id}", response_model=UserRead)
def update_user(id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return user.update_user(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user.delete_user(db, id)

