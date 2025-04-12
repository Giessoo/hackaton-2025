import hashlib
import uuid
import schemas
from models.User import User
from models.UserTeam import UserTeam
from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from auth import get_current_user

router = APIRouter()

@router.post("/user", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hashlib.sha256(user.password.encode()).hexdigest()
    token = uuid.uuid4().hex

    db_user = User(**user.dict(), token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/user", response_model=list[schemas.UserOut ])
async def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(User).all()

@router.put("/user/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.name:
        db_user.name = user.name
    if user.phone:
        db_user.phone = user.phone
    if user.password:
        db_user.password = hashlib.sha256(user.password.encode()).hexdigest()

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    
    return {"detail": "Пользователь удален"}