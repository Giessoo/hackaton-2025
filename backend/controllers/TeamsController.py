import schemas
from models.Team import Team
from models.UserTeam import UserTeam
from models.User import User
from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from auth import get_current_user

router = APIRouter()

@router.post("/team", response_model=schemas.TeamOut)
async def create_user(team: schemas.TeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    return db_team

@router.post("/userteam", response_model=schemas.UserTeamOut)
async def create_userteam(team: schemas.UserTeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = UserTeam(**team.dict())
    db.add(db_userteam)
    db.commit()
    db.refresh(db_userteam)
    
    return db_userteam

@router.get("/userteam", response_model=list[schemas.UserTeamOut ])
async def get_userteams(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(UserTeam).all()

@router.get("/userteam/{userteam_id}", response_model=schemas.UserTeamOut)
async def get_teams_by_id(userteam_id : int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = db.query(UserTeam).filter(UserTeam.id == userteam_id).first()
    if not db_userteam:
        raise HTTPException(status_code=404, detail="UserTeam not found")
    
    return db_userteam

@router.put("/userteam/{userteam_id}", response_model=schemas.UserTeamOut)
async def update_team(userteam_id: int, userteam: schemas.UserTeamBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = db.query(UserTeam).filter(UserTeam.id == userteam_id).first()
    if not db_userteam:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db_userteam.team_id = userteam.team_id
    db_userteam.user_id = userteam.user_id
    db.commit()
    db.refresh(db_userteam)
    
    return db_userteam

@router.delete("/userteam/{userteam_id}")
async def delete_user(userteam_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_userteam = db.query(UserTeam).filter(UserTeam.id == userteam_id).first()
    if not db_userteam:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(db_userteam)
    db.commit()
    
    return {"detail": "Отношение 'Бригада-сотрудник' удалено"}

@router.get("/team", response_model=list[schemas.TeamOut ])
async def get_teams(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Team).all()

@router.get("/team/{team_id}", response_model=schemas.TeamOut)
async def get_teams_by_id(team_id : int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return db_team

@router.put("/team/{team_id}", response_model=schemas.TeamOut)
async def update_team(team_id: int, team: schemas.TeamBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db_team.status = team.status
    db_team.title = team.title
    db.commit()
    db.refresh(db_team)
    
    return db_team

@router.delete("/team/{team_id}")
async def delete_user(team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(db_team)
    db.commit()
    
    return {"detail": "Бригада удалена"}