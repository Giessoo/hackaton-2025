from typing import Optional
from sqlalchemy.orm import Session
from models.UserTeam import UserTeam
from schemas import UserTeamCreate, UserTeamBase


def create_user_team(user_team_data: UserTeamCreate, db: Session) -> UserTeam:
    db_user_team = UserTeam(**user_team_data.dict())
    db.add(db_user_team)
    db.commit()
    db.refresh(db_user_team)
    return db_user_team


def get_user_team_by_id(userteam_id: int, db: Session) -> Optional[UserTeam]:
    return db.query(UserTeam).filter(UserTeam.id == userteam_id).first()


def get_all_user_teams(db: Session) -> list[UserTeam]:
    return db.query(UserTeam).all()


def update_user_team(user_team: UserTeam, update_data: UserTeamBase, db: Session) -> UserTeam:
    for field, value in update_data.dict().items():
        setattr(user_team, field, value)
    db.commit()
    db.refresh(user_team)
    return user_team


def delete_user_team(user_team: UserTeam, db: Session) -> None:
    db.delete(user_team)
    db.commit()
