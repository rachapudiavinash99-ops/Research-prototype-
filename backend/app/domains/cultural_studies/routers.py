from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import CulturalStudiesExperimentCreate, CulturalStudiesExperimentUpdate, CulturalStudiesExperimentResponse, CulturalStudiesFindingCreate, CulturalStudiesFindingResponse, CulturalStudiesDataPointCreate, CulturalStudiesDataPointResponse
from .services import CulturalStudiesService

router = APIRouter(prefix="/cultural_studies", tags=["CulturalStudies"])

def get_service(db: Session = Depends(get_db)) -> CulturalStudiesService:
    return CulturalStudiesService(db)

@router.post("/experiments", response_model=CulturalStudiesExperimentResponse)
def create_experiment(exp_in: CulturalStudiesExperimentCreate, service: CulturalStudiesService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[CulturalStudiesExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: CulturalStudiesService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=CulturalStudiesExperimentResponse)
def get_experiment(experiment_id: int, service: CulturalStudiesService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=CulturalStudiesExperimentResponse)
def update_experiment(experiment_id: int, exp_in: CulturalStudiesExperimentUpdate, service: CulturalStudiesService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: CulturalStudiesService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=CulturalStudiesFindingResponse)
def create_finding(finding_in: CulturalStudiesFindingCreate, service: CulturalStudiesService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[CulturalStudiesFindingResponse])
def get_findings(experiment_id: int, service: CulturalStudiesService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=CulturalStudiesDataPointResponse)
def create_datapoint(dp_in: CulturalStudiesDataPointCreate, service: CulturalStudiesService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[CulturalStudiesDataPointResponse])
def get_datapoints(experiment_id: int, service: CulturalStudiesService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
