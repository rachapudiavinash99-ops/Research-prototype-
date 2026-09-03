from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import HistoryExperimentCreate, HistoryExperimentUpdate, HistoryExperimentResponse, HistoryFindingCreate, HistoryFindingResponse, HistoryDataPointCreate, HistoryDataPointResponse
from .services import HistoryService

router = APIRouter(prefix="/history", tags=["History"])

def get_service(db: Session = Depends(get_db)) -> HistoryService:
    return HistoryService(db)

@router.post("/experiments", response_model=HistoryExperimentResponse)
def create_experiment(exp_in: HistoryExperimentCreate, service: HistoryService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[HistoryExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: HistoryService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=HistoryExperimentResponse)
def get_experiment(experiment_id: int, service: HistoryService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=HistoryExperimentResponse)
def update_experiment(experiment_id: int, exp_in: HistoryExperimentUpdate, service: HistoryService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: HistoryService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=HistoryFindingResponse)
def create_finding(finding_in: HistoryFindingCreate, service: HistoryService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[HistoryFindingResponse])
def get_findings(experiment_id: int, service: HistoryService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=HistoryDataPointResponse)
def create_datapoint(dp_in: HistoryDataPointCreate, service: HistoryService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[HistoryDataPointResponse])
def get_datapoints(experiment_id: int, service: HistoryService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
