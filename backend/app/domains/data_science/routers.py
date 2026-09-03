from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import DataScienceExperimentCreate, DataScienceExperimentUpdate, DataScienceExperimentResponse, DataScienceFindingCreate, DataScienceFindingResponse, DataScienceDataPointCreate, DataScienceDataPointResponse
from .services import DataScienceService

router = APIRouter(prefix="/data_science", tags=["DataScience"])

def get_service(db: Session = Depends(get_db)) -> DataScienceService:
    return DataScienceService(db)

@router.post("/experiments", response_model=DataScienceExperimentResponse)
def create_experiment(exp_in: DataScienceExperimentCreate, service: DataScienceService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[DataScienceExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: DataScienceService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=DataScienceExperimentResponse)
def get_experiment(experiment_id: int, service: DataScienceService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=DataScienceExperimentResponse)
def update_experiment(experiment_id: int, exp_in: DataScienceExperimentUpdate, service: DataScienceService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: DataScienceService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=DataScienceFindingResponse)
def create_finding(finding_in: DataScienceFindingCreate, service: DataScienceService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[DataScienceFindingResponse])
def get_findings(experiment_id: int, service: DataScienceService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=DataScienceDataPointResponse)
def create_datapoint(dp_in: DataScienceDataPointCreate, service: DataScienceService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[DataScienceDataPointResponse])
def get_datapoints(experiment_id: int, service: DataScienceService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
