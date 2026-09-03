from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import HumanFactorsExperimentCreate, HumanFactorsExperimentUpdate, HumanFactorsExperimentResponse, HumanFactorsFindingCreate, HumanFactorsFindingResponse, HumanFactorsDataPointCreate, HumanFactorsDataPointResponse
from .services import HumanFactorsService

router = APIRouter(prefix="/human_factors", tags=["HumanFactors"])

def get_service(db: Session = Depends(get_db)) -> HumanFactorsService:
    return HumanFactorsService(db)

@router.post("/experiments", response_model=HumanFactorsExperimentResponse)
def create_experiment(exp_in: HumanFactorsExperimentCreate, service: HumanFactorsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[HumanFactorsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: HumanFactorsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=HumanFactorsExperimentResponse)
def get_experiment(experiment_id: int, service: HumanFactorsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=HumanFactorsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: HumanFactorsExperimentUpdate, service: HumanFactorsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: HumanFactorsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=HumanFactorsFindingResponse)
def create_finding(finding_in: HumanFactorsFindingCreate, service: HumanFactorsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[HumanFactorsFindingResponse])
def get_findings(experiment_id: int, service: HumanFactorsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=HumanFactorsDataPointResponse)
def create_datapoint(dp_in: HumanFactorsDataPointCreate, service: HumanFactorsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[HumanFactorsDataPointResponse])
def get_datapoints(experiment_id: int, service: HumanFactorsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
