from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pos.repository.user import user_repository
from pos.schemas.user import UserCreate, UserUpdate
from pos.models.user import User
from datetime import datetime, timedelta, timezone
import jwt
from pos.core.config import security_settings
from pos.schemas.auth import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


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
    plain_password = user_dict.pop("password")
    
    user_dict["masked_password"] = hash_password(plain_password)
    
    return user_repository.create(db, user_dict)

def update_user(db: Session, id: int, data: UserUpdate) -> User:
    user = get_user(db, id)
    update_data = data.model_dump(exclude_unset=True)

    if "password" in update_data:
        plain_password = update_data.pop("password")
        update_data["masked_password"] = hash_password(plain_password)
        
    return user_repository.update(db, user, update_data)

def delete_user(db: Session, id: int) -> None:
    user = get_user(db, id)
    user_repository.delete(db, user)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=security_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, security_settings.SECRET_KEY, algorithm=security_settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, username: str, plain_password: str) -> User | None:
    user = user_repository.get_by_username(db, username)
    if not user:
        return None
    if not verify_password(plain_password, user.masked_password):
        return None
    return user
