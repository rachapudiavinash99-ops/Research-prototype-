from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import CommunicationStudiesExperimentCreate, CommunicationStudiesExperimentUpdate, CommunicationStudiesExperimentResponse, CommunicationStudiesFindingCreate, CommunicationStudiesFindingResponse, CommunicationStudiesDataPointCreate, CommunicationStudiesDataPointResponse
from .services import CommunicationStudiesService

router = APIRouter(prefix="/communication_studies", tags=["CommunicationStudies"])

def get_service(db: Session = Depends(get_db)) -> CommunicationStudiesService:
    return CommunicationStudiesService(db)

@router.post("/experiments", response_model=CommunicationStudiesExperimentResponse)
def create_experiment(exp_in: CommunicationStudiesExperimentCreate, service: CommunicationStudiesService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[CommunicationStudiesExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: CommunicationStudiesService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=CommunicationStudiesExperimentResponse)
def get_experiment(experiment_id: int, service: CommunicationStudiesService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=CommunicationStudiesExperimentResponse)
def update_experiment(experiment_id: int, exp_in: CommunicationStudiesExperimentUpdate, service: CommunicationStudiesService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: CommunicationStudiesService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=CommunicationStudiesFindingResponse)
def create_finding(finding_in: CommunicationStudiesFindingCreate, service: CommunicationStudiesService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[CommunicationStudiesFindingResponse])
def get_findings(experiment_id: int, service: CommunicationStudiesService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=CommunicationStudiesDataPointResponse)
def create_datapoint(dp_in: CommunicationStudiesDataPointCreate, service: CommunicationStudiesService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[CommunicationStudiesDataPointResponse])
def get_datapoints(experiment_id: int, service: CommunicationStudiesService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
