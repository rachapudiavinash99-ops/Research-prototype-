from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import BiologyExperimentCreate, BiologyExperimentUpdate, BiologyExperimentResponse, BiologyFindingCreate, BiologyFindingResponse, BiologyDataPointCreate, BiologyDataPointResponse
from .services import BiologyService

router = APIRouter(prefix="/biology", tags=["Biology"])

def get_service(db: Session = Depends(get_db)) -> BiologyService:
    return BiologyService(db)

@router.post("/experiments", response_model=BiologyExperimentResponse)
def create_experiment(exp_in: BiologyExperimentCreate, service: BiologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[BiologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: BiologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=BiologyExperimentResponse)
def get_experiment(experiment_id: int, service: BiologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=BiologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: BiologyExperimentUpdate, service: BiologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: BiologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=BiologyFindingResponse)
def create_finding(finding_in: BiologyFindingCreate, service: BiologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[BiologyFindingResponse])
def get_findings(experiment_id: int, service: BiologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=BiologyDataPointResponse)
def create_datapoint(dp_in: BiologyDataPointCreate, service: BiologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[BiologyDataPointResponse])
def get_datapoints(experiment_id: int, service: BiologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
