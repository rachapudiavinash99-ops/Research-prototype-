import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# Models: Prototype, Experiment
prototype_model_code = '''from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class PrototypeStatus(str, enum.Enum):
    idea = "idea"
    design = "design"
    development = "development"
    experiment = "experiment"
    testing = "testing"
    evaluation = "evaluation"
    accepted = "accepted"
    rejected = "rejected"
    archived = "archived"

class ExperimentStatus(str, enum.Enum):
    planned = "planned"
    running = "running"
    successful = "successful"
    failed = "failed"
    inconclusive = "inconclusive"

class Prototype(Base):
    __tablename__ = "prototypes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    version = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(Enum(PrototypeStatus), default=PrototypeStatus.idea)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    project = relationship("Project")

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    objective = Column(Text)
    prototype_id = Column(Integer, ForeignKey("prototypes.id"))
    status = Column(Enum(ExperimentStatus), default=ExperimentStatus.planned)
    result_metrics = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    prototype = relationship("Prototype")
'''
write_file("backend/app/models/prototype.py", prototype_model_code)
write_file("backend/app/db/base.py", '''from app.db.session import Base\nfrom app.models.user import User\nfrom app.models.project import Project, Topic\nfrom app.models.task import Task\nfrom app.models.prototype import Prototype, Experiment\n''')

# Schemas
prototype_schema_code = '''from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.prototype import PrototypeStatus, ExperimentStatus

class PrototypeBase(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    project_id: int
    status: PrototypeStatus = PrototypeStatus.idea

class PrototypeCreate(PrototypeBase):
    pass

class PrototypeResponse(PrototypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class ExperimentBase(BaseModel):
    name: str
    objective: Optional[str] = None
    prototype_id: int
    status: ExperimentStatus = ExperimentStatus.planned

class ExperimentCreate(ExperimentBase):
    pass

class ExperimentResponse(ExperimentBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
'''
write_file("backend/app/schemas/prototype.py", prototype_schema_code)

# API: Prototypes
prototype_api_code = '''from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.prototype import PrototypeCreate, PrototypeResponse, ExperimentCreate, ExperimentResponse
from app.models.prototype import Prototype, Experiment
from app.models.user import User
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/prototypes", response_model=PrototypeResponse)
def create_prototype(prototype: PrototypeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_proto = Prototype(**prototype.model_dump())
    db.add(db_proto)
    db.commit()
    db.refresh(db_proto)
    return db_proto

@router.post("/experiments", response_model=ExperimentResponse)
def create_experiment(experiment: ExperimentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_exp = Experiment(**experiment.model_dump())
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp
'''
write_file("backend/app/api/endpoints/prototypes.py", prototype_api_code)

# Update main
main_update = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, projects, tasks, prototypes
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
app.include_router(prototypes.router, prefix="/api", tags=["prototypes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Research Prototype Hub API"}
'''
write_file("backend/app/main.py", main_update)

print("Phase 5 Backend scaffolding complete")
