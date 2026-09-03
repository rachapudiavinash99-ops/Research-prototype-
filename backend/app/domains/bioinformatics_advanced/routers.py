from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import BioinformaticsAdvancedExperimentCreate, BioinformaticsAdvancedExperimentUpdate, BioinformaticsAdvancedExperimentResponse, BioinformaticsAdvancedFindingCreate, BioinformaticsAdvancedFindingResponse, BioinformaticsAdvancedDataPointCreate, BioinformaticsAdvancedDataPointResponse
from .services import BioinformaticsAdvancedService

router = APIRouter(prefix="/bioinformatics_advanced", tags=["BioinformaticsAdvanced"])

def get_service(db: Session = Depends(get_db)) -> BioinformaticsAdvancedService:
    return BioinformaticsAdvancedService(db)

@router.post("/experiments", response_model=BioinformaticsAdvancedExperimentResponse)
def create_experiment(exp_in: BioinformaticsAdvancedExperimentCreate, service: BioinformaticsAdvancedService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[BioinformaticsAdvancedExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: BioinformaticsAdvancedService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=BioinformaticsAdvancedExperimentResponse)
def get_experiment(experiment_id: int, service: BioinformaticsAdvancedService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=BioinformaticsAdvancedExperimentResponse)
def update_experiment(experiment_id: int, exp_in: BioinformaticsAdvancedExperimentUpdate, service: BioinformaticsAdvancedService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: BioinformaticsAdvancedService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=BioinformaticsAdvancedFindingResponse)
def create_finding(finding_in: BioinformaticsAdvancedFindingCreate, service: BioinformaticsAdvancedService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[BioinformaticsAdvancedFindingResponse])
def get_findings(experiment_id: int, service: BioinformaticsAdvancedService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=BioinformaticsAdvancedDataPointResponse)
def create_datapoint(dp_in: BioinformaticsAdvancedDataPointCreate, service: BioinformaticsAdvancedService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[BioinformaticsAdvancedDataPointResponse])
def get_datapoints(experiment_id: int, service: BioinformaticsAdvancedService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
