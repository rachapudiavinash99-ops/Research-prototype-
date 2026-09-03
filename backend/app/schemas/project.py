from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.project import ProjectStatus
from app.schemas.user import UserResponse

class TopicBase(BaseModel):
    name: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    topic_id: Optional[int] = None
    status: ProjectStatus = ProjectStatus.planning

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner: UserResponse
    topic: Optional[TopicResponse]
    members: List[UserResponse] = []
    class Config:
        from_attributes = True
