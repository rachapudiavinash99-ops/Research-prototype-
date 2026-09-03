from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import EconomicsExperimentCreate, EconomicsExperimentUpdate, EconomicsExperimentResponse, EconomicsFindingCreate, EconomicsFindingResponse, EconomicsDataPointCreate, EconomicsDataPointResponse
from .services import EconomicsService

router = APIRouter(prefix="/economics", tags=["Economics"])

def get_service(db: Session = Depends(get_db)) -> EconomicsService:
    return EconomicsService(db)

@router.post("/experiments", response_model=EconomicsExperimentResponse)
def create_experiment(exp_in: EconomicsExperimentCreate, service: EconomicsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[EconomicsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: EconomicsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=EconomicsExperimentResponse)
def get_experiment(experiment_id: int, service: EconomicsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=EconomicsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: EconomicsExperimentUpdate, service: EconomicsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: EconomicsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=EconomicsFindingResponse)
def create_finding(finding_in: EconomicsFindingCreate, service: EconomicsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[EconomicsFindingResponse])
def get_findings(experiment_id: int, service: EconomicsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=EconomicsDataPointResponse)
def create_datapoint(dp_in: EconomicsDataPointCreate, service: EconomicsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[EconomicsDataPointResponse])
def get_datapoints(experiment_id: int, service: EconomicsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
