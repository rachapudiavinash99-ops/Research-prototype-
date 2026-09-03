from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import SoilScienceExperimentCreate, SoilScienceExperimentUpdate, SoilScienceExperimentResponse, SoilScienceFindingCreate, SoilScienceFindingResponse, SoilScienceDataPointCreate, SoilScienceDataPointResponse
from .services import SoilScienceService

router = APIRouter(prefix="/soil_science", tags=["SoilScience"])

def get_service(db: Session = Depends(get_db)) -> SoilScienceService:
    return SoilScienceService(db)

@router.post("/experiments", response_model=SoilScienceExperimentResponse)
def create_experiment(exp_in: SoilScienceExperimentCreate, service: SoilScienceService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[SoilScienceExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: SoilScienceService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=SoilScienceExperimentResponse)
def get_experiment(experiment_id: int, service: SoilScienceService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=SoilScienceExperimentResponse)
def update_experiment(experiment_id: int, exp_in: SoilScienceExperimentUpdate, service: SoilScienceService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: SoilScienceService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=SoilScienceFindingResponse)
def create_finding(finding_in: SoilScienceFindingCreate, service: SoilScienceService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[SoilScienceFindingResponse])
def get_findings(experiment_id: int, service: SoilScienceService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=SoilScienceDataPointResponse)
def create_datapoint(dp_in: SoilScienceDataPointCreate, service: SoilScienceService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[SoilScienceDataPointResponse])
def get_datapoints(experiment_id: int, service: SoilScienceService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
