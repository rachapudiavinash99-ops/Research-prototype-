from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import PublicHealthExperimentCreate, PublicHealthExperimentUpdate, PublicHealthExperimentResponse, PublicHealthFindingCreate, PublicHealthFindingResponse, PublicHealthDataPointCreate, PublicHealthDataPointResponse
from .services import PublicHealthService

router = APIRouter(prefix="/public_health", tags=["PublicHealth"])

def get_service(db: Session = Depends(get_db)) -> PublicHealthService:
    return PublicHealthService(db)

@router.post("/experiments", response_model=PublicHealthExperimentResponse)
def create_experiment(exp_in: PublicHealthExperimentCreate, service: PublicHealthService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[PublicHealthExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: PublicHealthService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=PublicHealthExperimentResponse)
def get_experiment(experiment_id: int, service: PublicHealthService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=PublicHealthExperimentResponse)
def update_experiment(experiment_id: int, exp_in: PublicHealthExperimentUpdate, service: PublicHealthService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: PublicHealthService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=PublicHealthFindingResponse)
def create_finding(finding_in: PublicHealthFindingCreate, service: PublicHealthService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[PublicHealthFindingResponse])
def get_findings(experiment_id: int, service: PublicHealthService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=PublicHealthDataPointResponse)
def create_datapoint(dp_in: PublicHealthDataPointCreate, service: PublicHealthService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[PublicHealthDataPointResponse])
def get_datapoints(experiment_id: int, service: PublicHealthService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
