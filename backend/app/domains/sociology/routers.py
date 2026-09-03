from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import SociologyExperimentCreate, SociologyExperimentUpdate, SociologyExperimentResponse, SociologyFindingCreate, SociologyFindingResponse, SociologyDataPointCreate, SociologyDataPointResponse
from .services import SociologyService

router = APIRouter(prefix="/sociology", tags=["Sociology"])

def get_service(db: Session = Depends(get_db)) -> SociologyService:
    return SociologyService(db)

@router.post("/experiments", response_model=SociologyExperimentResponse)
def create_experiment(exp_in: SociologyExperimentCreate, service: SociologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[SociologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: SociologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=SociologyExperimentResponse)
def get_experiment(experiment_id: int, service: SociologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=SociologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: SociologyExperimentUpdate, service: SociologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: SociologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=SociologyFindingResponse)
def create_finding(finding_in: SociologyFindingCreate, service: SociologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[SociologyFindingResponse])
def get_findings(experiment_id: int, service: SociologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=SociologyDataPointResponse)
def create_datapoint(dp_in: SociologyDataPointCreate, service: SociologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[SociologyDataPointResponse])
def get_datapoints(experiment_id: int, service: SociologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
