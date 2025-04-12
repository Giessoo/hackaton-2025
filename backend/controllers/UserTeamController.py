import schemas
from models.User import User
from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from auth import get_current_user
import repositories.UserTeamRepository as UserTeamRepository

router = APIRouter()

@router.post("/userteam", response_model=schemas.UserTeamOut)
async def create_userteam(team: schemas.UserTeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_team_repo.create_user_team(team, db)

@router.get("/userteam", response_model=list[schemas.UserTeamOut])
async def get_userteams(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserTeamRepository.get_all_user_teams(db)

@router.get("/userteam/{userteam_id}", response_model=schemas.UserTeamOut)
async def get_teams_by_id(userteam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = UserTeamRepository.get_user_team_by_id(userteam_id, db)
    if not db_userteam:
        raise HTTPException(status_code=404, detail="UserTeam not found")
    return db_userteam

@router.put("/userteam/{userteam_id}", response_model=schemas.UserTeamOut)
async def update_team(userteam_id: int, userteam: schemas.UserTeamBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = UserTeamRepository.get_user_team_by_id(userteam_id, db)
    if not db_userteam:
        raise HTTPException(status_code=404, detail="UserTeam not found")
    return UserTeamRepository.update_user_team(db_userteam, userteam, db)

@router.delete("/userteam/{userteam_id}")
async def delete_user(userteam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = UserTeamRepository.get_user_team_by_id(userteam_id, db)
    if not db_userteam:
        raise HTTPException(status_code=404, detail="UserTeam not found")
    UserTeamRepository.delete_user_team(db_userteam, db)
    return {"detail": "Отношение 'Бригада-сотрудник' удалено"}
