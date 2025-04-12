from typing import Optional
from sqlalchemy.orm import Session
from models.Team import Team
from schemas import TeamCreate, TeamBase


def create_team(team: TeamCreate, db: Session) -> Team:
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team_by_id(team_id: int, db: Session) -> Optional[Team]:
    return db.query(Team).filter(Team.id == team_id).first()


def get_all_teams(db: Session) -> list[Team]:
    return db.query(Team).all()


def update_team(team: Team, update_data: TeamBase, db: Session) -> Team:
    for field, value in update_data.dict().items():
        setattr(team, field, value)
    db.commit()
    db.refresh(team)
    return team


def delete_team(team: Team, db: Session) -> None:
    db.delete(team)
    db.commit()
