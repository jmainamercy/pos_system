from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pos.repository.user import user_repository
from pos.schemas.user import UserCreate, UserUpdate
from pos.models.user import User


def get_user(db: Session, id: int) -> User:
    user = user_repository.get(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with ID {id} does not exist"
        )
    return user

def list_users(db: Session) -> list[User]:
    return user_repository.get_all(db)

def create_user(db: Session, data: UserCreate) -> User:
    if user_repository.get_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Username is already taken by another employee"
        )

    user_dict = data.model_dump()
    return user_repository.create(db, user_dict)

def update_user(db: Session, id: int, data: UserUpdate) -> User:
    user = get_user(db, id)
    update_data = data.model_dump(exclude_unset=True)
        
    return user_repository.update(db, user, update_data)

def delete_user(db: Session, id: int) -> None:
    user = get_user(db, id)
    user_repository.delete(db, user)

