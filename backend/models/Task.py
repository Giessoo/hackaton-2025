from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger, TIMESTAMP, func
from sqlalchemy.orm import relationship
from db.database import Base
from models.Team import Team

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(SmallInteger, nullable=True)
    address = Column(String(255), nullable=True)
    device_type = Column(String(255), nullable=True)
    device_num = Column(Integer, nullable=True)
    status = Column(SmallInteger, nullable=True)
    photo = Column(String(255), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Связь с таблицей teams
    team = relationship("Team") 