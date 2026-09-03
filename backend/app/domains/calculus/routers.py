from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import CalculusExperimentCreate, CalculusExperimentUpdate, CalculusExperimentResponse, CalculusFindingCreate, CalculusFindingResponse, CalculusDataPointCreate, CalculusDataPointResponse
from .services import CalculusService

router = APIRouter(prefix="/calculus", tags=["Calculus"])

def get_service(db: Session = Depends(get_db)) -> CalculusService:
    return CalculusService(db)

@router.post("/experiments", response_model=CalculusExperimentResponse)
def create_experiment(exp_in: CalculusExperimentCreate, service: CalculusService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[CalculusExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: CalculusService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=CalculusExperimentResponse)
def get_experiment(experiment_id: int, service: CalculusService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=CalculusExperimentResponse)
def update_experiment(experiment_id: int, exp_in: CalculusExperimentUpdate, service: CalculusService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: CalculusService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=CalculusFindingResponse)
def create_finding(finding_in: CalculusFindingCreate, service: CalculusService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[CalculusFindingResponse])
def get_findings(experiment_id: int, service: CalculusService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=CalculusDataPointResponse)
def create_datapoint(dp_in: CalculusDataPointCreate, service: CalculusService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[CalculusDataPointResponse])
def get_datapoints(experiment_id: int, service: CalculusService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
