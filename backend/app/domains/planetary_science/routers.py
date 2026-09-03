from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import PlanetaryScienceExperimentCreate, PlanetaryScienceExperimentUpdate, PlanetaryScienceExperimentResponse, PlanetaryScienceFindingCreate, PlanetaryScienceFindingResponse, PlanetaryScienceDataPointCreate, PlanetaryScienceDataPointResponse
from .services import PlanetaryScienceService

router = APIRouter(prefix="/planetary_science", tags=["PlanetaryScience"])

def get_service(db: Session = Depends(get_db)) -> PlanetaryScienceService:
    return PlanetaryScienceService(db)

@router.post("/experiments", response_model=PlanetaryScienceExperimentResponse)
def create_experiment(exp_in: PlanetaryScienceExperimentCreate, service: PlanetaryScienceService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[PlanetaryScienceExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: PlanetaryScienceService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=PlanetaryScienceExperimentResponse)
def get_experiment(experiment_id: int, service: PlanetaryScienceService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=PlanetaryScienceExperimentResponse)
def update_experiment(experiment_id: int, exp_in: PlanetaryScienceExperimentUpdate, service: PlanetaryScienceService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: PlanetaryScienceService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=PlanetaryScienceFindingResponse)
def create_finding(finding_in: PlanetaryScienceFindingCreate, service: PlanetaryScienceService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[PlanetaryScienceFindingResponse])
def get_findings(experiment_id: int, service: PlanetaryScienceService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=PlanetaryScienceDataPointResponse)
def create_datapoint(dp_in: PlanetaryScienceDataPointCreate, service: PlanetaryScienceService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[PlanetaryScienceDataPointResponse])
def get_datapoints(experiment_id: int, service: PlanetaryScienceService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
