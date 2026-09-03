from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import MaterialsScienceExperimentCreate, MaterialsScienceExperimentUpdate, MaterialsScienceExperimentResponse, MaterialsScienceFindingCreate, MaterialsScienceFindingResponse, MaterialsScienceDataPointCreate, MaterialsScienceDataPointResponse
from .services import MaterialsScienceService

router = APIRouter(prefix="/materials_science", tags=["MaterialsScience"])

def get_service(db: Session = Depends(get_db)) -> MaterialsScienceService:
    return MaterialsScienceService(db)

@router.post("/experiments", response_model=MaterialsScienceExperimentResponse)
def create_experiment(exp_in: MaterialsScienceExperimentCreate, service: MaterialsScienceService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[MaterialsScienceExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: MaterialsScienceService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=MaterialsScienceExperimentResponse)
def get_experiment(experiment_id: int, service: MaterialsScienceService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=MaterialsScienceExperimentResponse)
def update_experiment(experiment_id: int, exp_in: MaterialsScienceExperimentUpdate, service: MaterialsScienceService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: MaterialsScienceService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=MaterialsScienceFindingResponse)
def create_finding(finding_in: MaterialsScienceFindingCreate, service: MaterialsScienceService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[MaterialsScienceFindingResponse])
def get_findings(experiment_id: int, service: MaterialsScienceService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=MaterialsScienceDataPointResponse)
def create_datapoint(dp_in: MaterialsScienceDataPointCreate, service: MaterialsScienceService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[MaterialsScienceDataPointResponse])
def get_datapoints(experiment_id: int, service: MaterialsScienceService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
