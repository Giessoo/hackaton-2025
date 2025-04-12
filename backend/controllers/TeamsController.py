from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from auth import get_current_user
from models.User import User
import schemas
import repositories.TeamRepository as TeamRepository
import repositories.UserTeamRepository as UserTeamRepository

router = APIRouter()


@router.post("/team", response_model=schemas.TeamOut)
async def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TeamRepository.create_team(team, db)


@router.get("/team", response_model=list[schemas.TeamOut])
async def get_teams(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TeamRepository.get_all_teams(db)


@router.get("/team/{team_id}", response_model=schemas.TeamOut)
async def get_team_by_id(team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_team = TeamRepository.get_team_by_id(team_id, db)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.put("/team/{team_id}", response_model=schemas.TeamOut)
async def update_team_by_id(team_id: int, team_data: schemas.TeamBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_team = TeamRepository.get_team_by_id(team_id, db)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamRepository.update_team(db_team, team_data, db)


@router.delete("/team/{team_id}")
async def delete_team_by_id(team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_team = TeamRepository.get_team_by_id(team_id, db)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    TeamRepository.delete_team(db_team, db)
    return {"detail": "Бригада удалена"}


@router.post("/userteam", response_model=schemas.UserTeamOut)
async def create_user_team(user_team: schemas.UserTeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserTeamRepository.create_user_team(user_team, db)


@router.get("/userteam", response_model=list[schemas.UserTeamOut])
async def get_user_teams(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_team_repo.get_all_user_teams(db)


@router.get("/userteam/{userteam_id}", response_model=schemas.UserTeamOut)
async def get_user_team_by_id(userteam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = UserTeamRepository.get_user_team_by_id(userteam_id, db)
    if not db_userteam:
        raise HTTPException(status_code=404, detail="UserTeam not found")
    return db_userteam


@router.put("/userteam/{userteam_id}", response_model=schemas.UserTeamOut)
async def update_user_team_by_id(userteam_id: int, user_team_data: schemas.UserTeamBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = UserTeamRepository.get_user_team_by_id(userteam_id, db)
    if not db_userteam:
        raise HTTPException(status_code=404, detail="UserTeam not found")
    return UserTeamRepository.update_user_team(db_userteam, user_team_data, db)


@router.delete("/userteam/{userteam_id}")
async def delete_user_team_by_id(userteam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = UserTeamRepository.get_user_team_by_id(userteam_id, db)
    if not db_userteam:
        raise HTTPException(status_code=404, detail="UserTeam not found")
    UserTeamRepository.delete_user_team(db_userteam, db)
    return {"detail": "Отношение 'Бригада-сотрудник' удалено"}
