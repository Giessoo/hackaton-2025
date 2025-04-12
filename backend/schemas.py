from pydantic import BaseModel, constr
from typing import Literal, Optional, Dict
from datetime import datetime

# ---------- TASKS ----------
class TaskBase(BaseModel):
    task_type: Optional[int]
    address: Optional[str]
    device_type: Optional[str]
    device_num: Optional[int]
    status: Literal[0, 1, 2] = 0  # только допустимые статусы
    photo: Optional[str]
    team_id: Optional[int]

class TaskCreate(TaskBase):
    title: str
    address: str
    status: int

class TaskOut(TaskBase):
    id: int
    task_type: Optional[int]
    address: Optional[str]
    device_type: Optional[str]
    device_num: Optional[int]
    status: Optional[int]
    photo: Optional[str]
    team_id: Optional[int]

    class Config:
        orm_mode = True


# ---------- USERS ----------
class UserBase(BaseModel):
    name: Optional[str]
    phone: str
    password: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    name: str
    phone: str
    token: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ---------- TEAMS ----------
class TeamBase(BaseModel):
    title: Optional[str]
    status: Literal[0, 1] = 0

class TeamCreate(TeamBase):
    pass

class TeamOut(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ---------- USER_TEAMS ----------
class UserTeamBase(BaseModel):
    team_id: Optional[int]
    user_id: Optional[int]
    # status: Optional[int]

class UserTeamCreate(UserTeamBase):
    pass

class UserTeamOut(UserTeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True