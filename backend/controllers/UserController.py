import hashlib
import schemas
from models.User import User
from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

def generate_pin_code(full_name):
    normalized_name = full_name.lower().replace(" ", "")
    hash_object = hashlib.sha256(normalized_name.encode())
    hash_hex = hash_object.hexdigest()
    pin_code = int(hash_hex[:4], 16)
    pin_code = str(pin_code).zfill(4)
    
    return pin_code[:4]

@router.post("/user", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.pin = generate_pin_code(user.name)
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/user", response_model=list[schemas.UserOut ])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.put("/user/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User  not found")
    
    db_user.name = user.name
    db_user.pin = generate_pin_code(user.name)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.delete("/user/{user_id}", response_model=schemas.UserOut)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User  not found")
    
    db.delete(db_user)
    db.commit()
    
    return db_user