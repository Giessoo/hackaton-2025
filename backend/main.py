from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from models.Task import Task
import schemas

from db.database import Base

app = FastAPI()

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Dependency для сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
