from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

# ---------- TASKS ----------
class TaskBase(BaseModel):
    task_type: Optional[int]
    address: Optional[str]
    device_type: Optional[str]
    device_num: Optional[int]
    status: Optional[int]
    photo: Optional[str]
    team_id: Optional[int]

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ---------- USERS ----------
class UserBase(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    pin: Optional[int]  # как строка с 4 символами (ведущие нули сохраняются)

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ---------- TEAMS ----------
class TeamBase(BaseModel):
    title: Optional[str]
    status: Optional[int]

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
    status: Optional[int]

class UserTeamCreate(UserTeamBase):
    pass

class UserTeamOut(UserTeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
