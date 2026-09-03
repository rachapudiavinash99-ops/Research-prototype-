from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import VirologyExperimentCreate, VirologyExperimentUpdate, VirologyExperimentResponse, VirologyFindingCreate, VirologyFindingResponse, VirologyDataPointCreate, VirologyDataPointResponse
from .services import VirologyService

router = APIRouter(prefix="/virology", tags=["Virology"])

def get_service(db: Session = Depends(get_db)) -> VirologyService:
    return VirologyService(db)

@router.post("/experiments", response_model=VirologyExperimentResponse)
def create_experiment(exp_in: VirologyExperimentCreate, service: VirologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[VirologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: VirologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=VirologyExperimentResponse)
def get_experiment(experiment_id: int, service: VirologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=VirologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: VirologyExperimentUpdate, service: VirologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: VirologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=VirologyFindingResponse)
def create_finding(finding_in: VirologyFindingCreate, service: VirologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[VirologyFindingResponse])
def get_findings(experiment_id: int, service: VirologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=VirologyDataPointResponse)
def create_datapoint(dp_in: VirologyDataPointCreate, service: VirologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[VirologyDataPointResponse])
def get_datapoints(experiment_id: int, service: VirologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
