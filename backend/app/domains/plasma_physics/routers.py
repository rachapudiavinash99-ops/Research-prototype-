from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import PlasmaPhysicsExperimentCreate, PlasmaPhysicsExperimentUpdate, PlasmaPhysicsExperimentResponse, PlasmaPhysicsFindingCreate, PlasmaPhysicsFindingResponse, PlasmaPhysicsDataPointCreate, PlasmaPhysicsDataPointResponse
from .services import PlasmaPhysicsService

router = APIRouter(prefix="/plasma_physics", tags=["PlasmaPhysics"])

def get_service(db: Session = Depends(get_db)) -> PlasmaPhysicsService:
    return PlasmaPhysicsService(db)

@router.post("/experiments", response_model=PlasmaPhysicsExperimentResponse)
def create_experiment(exp_in: PlasmaPhysicsExperimentCreate, service: PlasmaPhysicsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[PlasmaPhysicsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: PlasmaPhysicsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=PlasmaPhysicsExperimentResponse)
def get_experiment(experiment_id: int, service: PlasmaPhysicsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=PlasmaPhysicsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: PlasmaPhysicsExperimentUpdate, service: PlasmaPhysicsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: PlasmaPhysicsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=PlasmaPhysicsFindingResponse)
def create_finding(finding_in: PlasmaPhysicsFindingCreate, service: PlasmaPhysicsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[PlasmaPhysicsFindingResponse])
def get_findings(experiment_id: int, service: PlasmaPhysicsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=PlasmaPhysicsDataPointResponse)
def create_datapoint(dp_in: PlasmaPhysicsDataPointCreate, service: PlasmaPhysicsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[PlasmaPhysicsDataPointResponse])
def get_datapoints(experiment_id: int, service: PlasmaPhysicsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
