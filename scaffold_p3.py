import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# Models: Project and Topic
project_model_code = '''from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class ProjectStatus(str, enum.Enum):
    planning = "planning"
    active = "active"
    experimenting = "experimenting"
    under_review = "under_review"
    completed = "completed"
    archived = "archived"

project_members = Table(
    'project_members', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    projects = relationship("Project", back_populates="topic")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    status = Column(Enum(ProjectStatus), default=ProjectStatus.planning)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User")
    topic = relationship("Topic", back_populates="projects")
    members = relationship("User", secondary=project_members)
'''
write_file("backend/app/models/project.py", project_model_code)
write_file("backend/app/db/base.py", '''from app.db.session import Base\nfrom app.models.user import User\nfrom app.models.project import Project, Topic\n''')

# Schemas
project_schema_code = '''from pydantic import BaseModel
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
'''
write_file("backend/app/schemas/project.py", project_schema_code)

# API: Projects
project_api_code = '''from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, TopicCreate, TopicResponse
from app.models.project import Project, Topic
from app.models.user import User
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/topics", response_model=TopicResponse)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_topic = Topic(**topic.model_dump())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.get("/topics", response_model=List[TopicResponse])
def get_topics(db: Session = Depends(get_db)):
    return db.query(Topic).all()

@router.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = Project(**project.model_dump(), owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Project).all()
'''
write_file("backend/app/api/endpoints/projects.py", project_api_code)

# Update main
main_update = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, projects
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Research Prototype Hub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api", tags=["projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Research Prototype Hub API"}
'''
write_file("backend/app/main.py", main_update)

print("Phase 3 Backend scaffolding complete")
