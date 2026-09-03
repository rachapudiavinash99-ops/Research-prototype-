import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# Models: Task
task_model_code = '''from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class TaskStatus(str, enum.Enum):
    backlog = "backlog"
    todo = "todo"
    in_progress = "in_progress"
    blocked = "blocked"
    review = "review"
    completed = "completed"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project")
    assignee = relationship("User")
'''
write_file("backend/app/models/task.py", task_model_code)
write_file("backend/app/db/base.py", '''from app.db.session import Base\nfrom app.models.user import User\nfrom app.models.project import Project, Topic\nfrom app.models.task import Task\n''')

# Schemas
task_schema_code = '''from pydantic import BaseModel
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
'''
write_file("backend/app/schemas/task.py", task_schema_code)

# API: Tasks
task_api_code = '''from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.models.task import Task
from app.models.user import User
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.project_id == project_id).all()
'''
write_file("backend/app/api/endpoints/tasks.py", task_api_code)

# Update main
main_update = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, projects, tasks
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
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Research Prototype Hub API"}
'''
write_file("backend/app/main.py", main_update)

print("Phase 4 Backend scaffolding complete")
