from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import CondensedMatterPhysicsExperimentCreate, CondensedMatterPhysicsExperimentUpdate, CondensedMatterPhysicsExperimentResponse, CondensedMatterPhysicsFindingCreate, CondensedMatterPhysicsFindingResponse, CondensedMatterPhysicsDataPointCreate, CondensedMatterPhysicsDataPointResponse
from .services import CondensedMatterPhysicsService

router = APIRouter(prefix="/condensed_matter_physics", tags=["CondensedMatterPhysics"])

def get_service(db: Session = Depends(get_db)) -> CondensedMatterPhysicsService:
    return CondensedMatterPhysicsService(db)

@router.post("/experiments", response_model=CondensedMatterPhysicsExperimentResponse)
def create_experiment(exp_in: CondensedMatterPhysicsExperimentCreate, service: CondensedMatterPhysicsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[CondensedMatterPhysicsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: CondensedMatterPhysicsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=CondensedMatterPhysicsExperimentResponse)
def get_experiment(experiment_id: int, service: CondensedMatterPhysicsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=CondensedMatterPhysicsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: CondensedMatterPhysicsExperimentUpdate, service: CondensedMatterPhysicsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: CondensedMatterPhysicsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=CondensedMatterPhysicsFindingResponse)
def create_finding(finding_in: CondensedMatterPhysicsFindingCreate, service: CondensedMatterPhysicsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[CondensedMatterPhysicsFindingResponse])
def get_findings(experiment_id: int, service: CondensedMatterPhysicsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=CondensedMatterPhysicsDataPointResponse)
def create_datapoint(dp_in: CondensedMatterPhysicsDataPointCreate, service: CondensedMatterPhysicsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[CondensedMatterPhysicsDataPointResponse])
def get_datapoints(experiment_id: int, service: CondensedMatterPhysicsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
