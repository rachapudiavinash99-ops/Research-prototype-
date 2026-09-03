from fastapi import APIRouter, Depends, HTTPException, status
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
