from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import ArchitectureExperimentCreate, ArchitectureExperimentUpdate, ArchitectureExperimentResponse, ArchitectureFindingCreate, ArchitectureFindingResponse, ArchitectureDataPointCreate, ArchitectureDataPointResponse
from .services import ArchitectureService

router = APIRouter(prefix="/architecture", tags=["Architecture"])

def get_service(db: Session = Depends(get_db)) -> ArchitectureService:
    return ArchitectureService(db)

@router.post("/experiments", response_model=ArchitectureExperimentResponse)
def create_experiment(exp_in: ArchitectureExperimentCreate, service: ArchitectureService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[ArchitectureExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: ArchitectureService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=ArchitectureExperimentResponse)
def get_experiment(experiment_id: int, service: ArchitectureService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=ArchitectureExperimentResponse)
def update_experiment(experiment_id: int, exp_in: ArchitectureExperimentUpdate, service: ArchitectureService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: ArchitectureService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=ArchitectureFindingResponse)
def create_finding(finding_in: ArchitectureFindingCreate, service: ArchitectureService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[ArchitectureFindingResponse])
def get_findings(experiment_id: int, service: ArchitectureService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=ArchitectureDataPointResponse)
def create_datapoint(dp_in: ArchitectureDataPointCreate, service: ArchitectureService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[ArchitectureDataPointResponse])
def get_datapoints(experiment_id: int, service: ArchitectureService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
