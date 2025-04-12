import os
import json
import base64
import zipfile
import io
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from db.database import get_db
from models.Task import Task
import schemas
router = APIRouter()

UPLOAD_FOLDER = "storage"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_file(file: UploadFile) -> str:
    filename = f"{uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path

@router.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# @router.get("/tasks", response_model=list[schemas.TaskOut])
# def get_tasks(db: Session = Depends(get_db)):
#     tasks = db.query(Task).all()
#     for task in tasks:
#         if task.photo:
#             task.photo = task.photo
#     return tasks

@router.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks_with_files(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    for task in tasks:
        if task.photo:
            try:
                # Парсим JSON строку
                photo_paths = json.loads(task.photo)
                
                # Обрабатываем каждый путь
                result = {}
                for key, path in photo_paths.items():
                    try:
                        with open(path, "rb") as file:
                            result[key] = base64.b64encode(file.read()).decode('utf-8')
                    except Exception as file_error:
                        # Если не удалось прочитать файл, оставляем оригинальный путь
                        result[key] = path
                
                # Преобразуем обратно в JSON строку
                task.photo = json.dumps(result)
            except json.JSONDecodeError:
                # Если это не JSON, оставляем как есть
                pass
    return tasks


# @router.get("/tasks/{task_id}", response_model=schemas.TaskOut)
# def get_task(task_id: int, db: Session = Depends(get_db)):
#     task = db.query(Task).filter(Task.id == task_id).first()
#     if not task:
#         raise HTTPException(status_code=404, detail="Задача не найдена")
#     if task.photo:
#         task.photo = task.photo
#     return task

@router.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    if task.photo:
        try:
            photo_paths = json.loads(task.photo)
            result = {}
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for key, path in photo_paths.items():
                    try:
                        zipf.write(path)
                        result[key] = "ZIPPED"  # Маркер, что файл в архиве
                    except Exception:
                        result[key] = path  # Оригинальный путь при ошибке
            
            zip_buffer.seek(0)
            zip_base64 = base64.b64encode(zip_buffer.read()).decode('utf-8')
            result['_zip'] = zip_base64  # Добавляем архив к результату
            task.photo = json.dumps(result)
            
        except Exception as e:
            print("Exception!")
            with open(task.photo, "rb") as file:
                task.photo = base64.b64encode(file.read()).decode('utf-8')
    
    return task


@router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
async def update_task(
    task_id: int,
    title: Optional[str] = Form(None),
    status: int = Form(...),
    task_type: Optional[int] = Form(None),
    address: Optional[str] = Form(None),
    device_type: Optional[str] = Form(None),
    device_num: Optional[int] = Form(None),
    team_id: Optional[int] = Form(None),
    before_photo: UploadFile = File(None),
    after_photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # Сохраняем фото
    photo_paths = {}
    if before_photo:
        photo_paths["before"] = save_file(before_photo)
    if after_photo:
        photo_paths["after"] = save_file(after_photo)

    # Обновляем поля
    task.title = title
    task.status = status
    task.task_type = task_type
    task.address = address
    task.device_type = device_type
    task.device_num = device_num
    task.team_id = team_id

    if photo_paths:
        task.photo = json.dumps(photo_paths)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    db.delete(task)
    db.commit()
    return {"detail": "Задача удалена"}
