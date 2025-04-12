from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import hashlib

from db.database import get_db
from models.User import User
import schemas

router = APIRouter()

@router.post("/auth", response_model=schemas.UserOut)
async def login(user: schemas.UserBase, db: Session = Depends(get_db)):
    if not user.phone or not user.password:
        raise HTTPException(status_code=400, detail="Phone and password are required")

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    db_user = db.query(User).filter(
        User.phone == user.phone,
        User.password == hashed_password
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid phone or password")

    # Генерация нового токена
    db_user.token = str(uuid4())
    db.commit()
    db.refresh(db_user)

    return db_user
