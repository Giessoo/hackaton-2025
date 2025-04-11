import schemas
from models.Team import Team
from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/team", response_model=schemas.TeamOut)
async def create_user(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    return db_team

@router.get("/team", response_model=list[schemas.TeamOut ])
async def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()

@router.put("/team/{team_id}", response_model=schemas.TeamOut)
async def update_team(team_id: int, team: schemas.TeamBase, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db_team.status = team.status
    db_team.title = team.title
    db.commit()
    db.refresh(db_team)
    
    return db_team

@router.delete("/team/{team_id}", response_model=schemas.TeamOut)
async def delete_user(team_id: int, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(db_team)
    db.commit()
    
    return db_team