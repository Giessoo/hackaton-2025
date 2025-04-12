import hashlib
import uuid
import schemas
from models.User import User
from models.UserTeam import UserTeam
from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from auth import get_current_user
import repositories.UserRepository as UserRepository

router = APIRouter()

@router.post("/user", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return UserRepository.create_user(user, db)


@router.get("/user", response_model=list[schemas.UserOut ])
async def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserRepository.get_all_users(db)

@router.put("/user/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRepository.update_user(db_user, user, db)

@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    UserRepository.delete_user(db_user, db)
    return {"detail": "Пользователь удален"}