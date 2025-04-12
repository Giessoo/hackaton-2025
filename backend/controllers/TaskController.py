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
from models.User import User
import schemas
from auth import get_current_user
import repositories.TaskRepository as TaskRepository

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
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TaskRepository.create_task(task, db)


@router.get("/tasks/{task_id}/users", response_model=list[schemas.UserOut])
def get_task_users(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(User).all()


@router.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks_with_files(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = TaskRepository.get_all_tasks(db)
    for task in tasks:
        if task.photo:
            try:
                photo_paths = json.loads(task.photo)
                result = {}
                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for key, path in photo_paths.items():
                        try:
                            zipf.write(path)
                            result[key] = "ZIPPED"
                        except Exception:
                            result[key] = path

                zip_buffer.seek(0)
                zip_base64 = base64.b64encode(zip_buffer.read()).decode('utf-8')
                result['_zip'] = zip_base64
                task.photo = json.dumps(result)

            except json.JSONDecodeError:
                try:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write(task.photo)
                    zip_buffer.seek(0)
                    task.photo = base64.b64encode(zip_buffer.read()).decode('utf-8')
                except Exception:
                    pass
    return tasks


@router.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = TaskRepository.get_task(task_id, db)
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
                        result[key] = "ZIPPED"
                    except Exception:
                        result[key] = path

            zip_buffer.seek(0)
            zip_base64 = base64.b64encode(zip_buffer.read()).decode('utf-8')
            result['_zip'] = zip_base64
            task.photo = json.dumps(result)

        except Exception:
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = TaskRepository.get_task(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    photo_paths = {}
    if before_photo:
        photo_paths["before"] = save_file(before_photo)
    if after_photo:
        photo_paths["after"] = save_file(after_photo)

    update_data = {
        "title": title,
        "status": status,
        "task_type": task_type,
        "address": address,
        "device_type": device_type,
        "device_num": device_num,
        "team_id": team_id,
    }

    if photo_paths:
        update_data["photo"] = json.dumps(photo_paths)

    return TaskRepository.update_task(task, update_data, db)


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = TaskRepository.delete_task(task_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"detail": "Задача удалена"}
