import hashlib
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from models.User import User
from schemas import UserCreate, UserBase


def create_user(user_data: UserCreate, db: Session) -> User:
    hashed_password = hashlib.sha256(user_data.password.encode()).hexdigest()
    token = uuid.uuid4().hex
    db_user = User(**user_data.dict(exclude={"password"}), password=hashed_password, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_id(user_id: int, db: Session) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def update_user(db_user: User, update_data: UserBase, db: Session) -> User:
    if update_data.name:
        db_user.name = update_data.name
    if update_data.phone:
        db_user.phone = update_data.phone
    if update_data.password:
        db_user.password = hashlib.sha256(update_data.password.encode()).hexdigest()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db_user: User, db: Session) -> None:
    db.delete(db_user)
    db.commit()
