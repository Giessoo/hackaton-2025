from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
from models import UserTeam, Task

class Team(Base):
    __tablename__ = "teams"

    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    status = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связь с таблицей tasks (один ко многим с tasks)
    tasks = relationship("Task", back_populates="team")

    # Связь с таблицей user_teams (многие ко многим с пользователями)
    user_teams = relationship("UserTeam", back_populates="team")
