from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import base64
import zipfile
import io
from fastapi.responses import JSONResponse
from db.database import get_db

router = APIRouter()

@router.get("/act/{act_id}")
async def get_act_control(act_id: int, db: Session = Depends(get_db)):
    if act_id == 1:
        filename = "act_control.docx"
    elif act_id == 2:
        filename = "act_restrictions.docx"
    else:
        raise HTTPException(
            status_code=400,
            detail="Акт не существует. Доступные ID: 1 (control) или 2 (restrictions)"
        )
    
    path = f"backend/storage/{filename}"
    
    try:
        with open(path, "rb") as file:
            file_content = file.read()
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Файл {filename} не найден"
        )
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(filename, file_content)
    
    zip_buffer.seek(0)
    zip_base64 = base64.b64encode(zip_buffer.read()).decode('utf-8')
    
    return JSONResponse(
        content={
            "status": "success",
            "filename": filename,
            "zip_base64": zip_base64,
            "message": "Файл успешно закодирован в base64 ZIP"
        }
    )