from sqlalchemy.orm import Session

from pos.models.user import User


class UserRepository:
    def __init__(self):
        self.model = User

    def get(self, db: Session, id: int) -> User | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(self.model).filter(self.model.username == username).first()

    def get_all(self, db: Session) -> list[User]:
        return db.query(self.model).all()

    def create(self, db: Session, data: dict) -> User:
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, data: dict) -> User:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: User) -> None:
        db.delete(db_obj)
        db.commit()


user_repository = UserRepository()
