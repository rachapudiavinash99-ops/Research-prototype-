from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import SyntheticBiologyExperimentCreate, SyntheticBiologyExperimentUpdate, SyntheticBiologyExperimentResponse, SyntheticBiologyFindingCreate, SyntheticBiologyFindingResponse, SyntheticBiologyDataPointCreate, SyntheticBiologyDataPointResponse
from .services import SyntheticBiologyService

router = APIRouter(prefix="/synthetic_biology", tags=["SyntheticBiology"])

def get_service(db: Session = Depends(get_db)) -> SyntheticBiologyService:
    return SyntheticBiologyService(db)

@router.post("/experiments", response_model=SyntheticBiologyExperimentResponse)
def create_experiment(exp_in: SyntheticBiologyExperimentCreate, service: SyntheticBiologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[SyntheticBiologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: SyntheticBiologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=SyntheticBiologyExperimentResponse)
def get_experiment(experiment_id: int, service: SyntheticBiologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=SyntheticBiologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: SyntheticBiologyExperimentUpdate, service: SyntheticBiologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: SyntheticBiologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=SyntheticBiologyFindingResponse)
def create_finding(finding_in: SyntheticBiologyFindingCreate, service: SyntheticBiologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[SyntheticBiologyFindingResponse])
def get_findings(experiment_id: int, service: SyntheticBiologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=SyntheticBiologyDataPointResponse)
def create_datapoint(dp_in: SyntheticBiologyDataPointCreate, service: SyntheticBiologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[SyntheticBiologyDataPointResponse])
def get_datapoints(experiment_id: int, service: SyntheticBiologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
