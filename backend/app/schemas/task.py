from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus
from app.schemas.user import UserResponse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    assignee_id: Optional[int] = None
    status: TaskStatus = TaskStatus.todo

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    assignee: Optional[UserResponse] = None
    class Config:
        from_attributes = True
