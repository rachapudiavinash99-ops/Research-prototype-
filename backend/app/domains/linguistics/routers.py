from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import LinguisticsExperimentCreate, LinguisticsExperimentUpdate, LinguisticsExperimentResponse, LinguisticsFindingCreate, LinguisticsFindingResponse, LinguisticsDataPointCreate, LinguisticsDataPointResponse
from .services import LinguisticsService

router = APIRouter(prefix="/linguistics", tags=["Linguistics"])

def get_service(db: Session = Depends(get_db)) -> LinguisticsService:
    return LinguisticsService(db)

@router.post("/experiments", response_model=LinguisticsExperimentResponse)
def create_experiment(exp_in: LinguisticsExperimentCreate, service: LinguisticsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[LinguisticsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: LinguisticsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=LinguisticsExperimentResponse)
def get_experiment(experiment_id: int, service: LinguisticsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=LinguisticsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: LinguisticsExperimentUpdate, service: LinguisticsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: LinguisticsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=LinguisticsFindingResponse)
def create_finding(finding_in: LinguisticsFindingCreate, service: LinguisticsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[LinguisticsFindingResponse])
def get_findings(experiment_id: int, service: LinguisticsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=LinguisticsDataPointResponse)
def create_datapoint(dp_in: LinguisticsDataPointCreate, service: LinguisticsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[LinguisticsDataPointResponse])
def get_datapoints(experiment_id: int, service: LinguisticsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
