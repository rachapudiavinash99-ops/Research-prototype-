from fastapi import APIRouter, Depends, HTTPException, status
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
