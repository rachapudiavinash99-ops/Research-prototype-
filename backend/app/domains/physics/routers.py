from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import PhysicsExperimentCreate, PhysicsExperimentUpdate, PhysicsExperimentResponse, PhysicsFindingCreate, PhysicsFindingResponse, PhysicsDataPointCreate, PhysicsDataPointResponse
from .services import PhysicsService

router = APIRouter(prefix="/physics", tags=["Physics"])

def get_service(db: Session = Depends(get_db)) -> PhysicsService:
    return PhysicsService(db)

@router.post("/experiments", response_model=PhysicsExperimentResponse)
def create_experiment(exp_in: PhysicsExperimentCreate, service: PhysicsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[PhysicsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: PhysicsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=PhysicsExperimentResponse)
def get_experiment(experiment_id: int, service: PhysicsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=PhysicsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: PhysicsExperimentUpdate, service: PhysicsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: PhysicsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=PhysicsFindingResponse)
def create_finding(finding_in: PhysicsFindingCreate, service: PhysicsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[PhysicsFindingResponse])
def get_findings(experiment_id: int, service: PhysicsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=PhysicsDataPointResponse)
def create_datapoint(dp_in: PhysicsDataPointCreate, service: PhysicsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[PhysicsDataPointResponse])
def get_datapoints(experiment_id: int, service: PhysicsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
