from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import ComputationalPhysicsExperimentCreate, ComputationalPhysicsExperimentUpdate, ComputationalPhysicsExperimentResponse, ComputationalPhysicsFindingCreate, ComputationalPhysicsFindingResponse, ComputationalPhysicsDataPointCreate, ComputationalPhysicsDataPointResponse
from .services import ComputationalPhysicsService

router = APIRouter(prefix="/computational_physics", tags=["ComputationalPhysics"])

def get_service(db: Session = Depends(get_db)) -> ComputationalPhysicsService:
    return ComputationalPhysicsService(db)

@router.post("/experiments", response_model=ComputationalPhysicsExperimentResponse)
def create_experiment(exp_in: ComputationalPhysicsExperimentCreate, service: ComputationalPhysicsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[ComputationalPhysicsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: ComputationalPhysicsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=ComputationalPhysicsExperimentResponse)
def get_experiment(experiment_id: int, service: ComputationalPhysicsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=ComputationalPhysicsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: ComputationalPhysicsExperimentUpdate, service: ComputationalPhysicsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: ComputationalPhysicsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=ComputationalPhysicsFindingResponse)
def create_finding(finding_in: ComputationalPhysicsFindingCreate, service: ComputationalPhysicsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[ComputationalPhysicsFindingResponse])
def get_findings(experiment_id: int, service: ComputationalPhysicsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=ComputationalPhysicsDataPointResponse)
def create_datapoint(dp_in: ComputationalPhysicsDataPointCreate, service: ComputationalPhysicsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[ComputationalPhysicsDataPointResponse])
def get_datapoints(experiment_id: int, service: ComputationalPhysicsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
