import json
from typing import Optional
from sqlalchemy.orm import Session
from models.Task import Task
from schemas import TaskCreate


def create_task(task: TaskCreate, db: Session) -> Task:
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(task_id: int, db: Session) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()


def delete_task(task_id: int, db: Session) -> bool:
    task = get_task(task_id, db)
    if task:
        db.delete(task)
        db.commit()
        return True
    return False


def update_task(task: Task, update_data: dict, db: Session) -> Task:
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task
