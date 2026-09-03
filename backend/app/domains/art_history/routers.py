from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import ArtHistoryExperimentCreate, ArtHistoryExperimentUpdate, ArtHistoryExperimentResponse, ArtHistoryFindingCreate, ArtHistoryFindingResponse, ArtHistoryDataPointCreate, ArtHistoryDataPointResponse
from .services import ArtHistoryService

router = APIRouter(prefix="/art_history", tags=["ArtHistory"])

def get_service(db: Session = Depends(get_db)) -> ArtHistoryService:
    return ArtHistoryService(db)

@router.post("/experiments", response_model=ArtHistoryExperimentResponse)
def create_experiment(exp_in: ArtHistoryExperimentCreate, service: ArtHistoryService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[ArtHistoryExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: ArtHistoryService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=ArtHistoryExperimentResponse)
def get_experiment(experiment_id: int, service: ArtHistoryService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=ArtHistoryExperimentResponse)
def update_experiment(experiment_id: int, exp_in: ArtHistoryExperimentUpdate, service: ArtHistoryService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: ArtHistoryService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=ArtHistoryFindingResponse)
def create_finding(finding_in: ArtHistoryFindingCreate, service: ArtHistoryService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[ArtHistoryFindingResponse])
def get_findings(experiment_id: int, service: ArtHistoryService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=ArtHistoryDataPointResponse)
def create_datapoint(dp_in: ArtHistoryDataPointCreate, service: ArtHistoryService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[ArtHistoryDataPointResponse])
def get_datapoints(experiment_id: int, service: ArtHistoryService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
