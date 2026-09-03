import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# Models: Finding, Dataset
finding_model_code = '''from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class ConfidenceLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    confidence = Column(Enum(ConfidenceLevel), default=ConfidenceLevel.medium)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    metadata_info = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
'''
write_file("backend/app/models/finding.py", finding_model_code)
write_file("backend/app/db/base.py", '''from app.db.session import Base\nfrom app.models.user import User\nfrom app.models.project import Project, Topic\nfrom app.models.task import Task\nfrom app.models.prototype import Prototype, Experiment\nfrom app.models.finding import Finding, Dataset\n''')

# Schemas
finding_schema_code = '''from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.finding import ConfidenceLevel

class FindingBase(BaseModel):
    title: str
    description: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.medium
    experiment_id: int

class FindingCreate(FindingBase):
    pass

class FindingResponse(FindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
'''
write_file("backend/app/schemas/finding.py", finding_schema_code)

# API: Findings
finding_api_code = '''from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.finding import FindingCreate, FindingResponse
from app.models.finding import Finding
from app.models.user import User
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/findings", response_model=FindingResponse)
def create_finding(finding: FindingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_find = Finding(**finding.model_dump())
    db.add(db_find)
    db.commit()
    db.refresh(db_find)
    return db_find
'''
write_file("backend/app/api/endpoints/findings.py", finding_api_code)

# Update main
main_update = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, projects, tasks, prototypes, findings
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
app.include_router(findings.router, prefix="/api", tags=["findings"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Research Prototype Hub API"}
'''
write_file("backend/app/main.py", main_update)

print("Phase 6 Backend scaffolding complete")
