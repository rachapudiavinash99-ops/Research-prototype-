from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import QuantumMechanicsAdvancedExperimentCreate, QuantumMechanicsAdvancedExperimentUpdate, QuantumMechanicsAdvancedExperimentResponse, QuantumMechanicsAdvancedFindingCreate, QuantumMechanicsAdvancedFindingResponse, QuantumMechanicsAdvancedDataPointCreate, QuantumMechanicsAdvancedDataPointResponse
from .services import QuantumMechanicsAdvancedService

router = APIRouter(prefix="/quantum_mechanics_advanced", tags=["QuantumMechanicsAdvanced"])

def get_service(db: Session = Depends(get_db)) -> QuantumMechanicsAdvancedService:
    return QuantumMechanicsAdvancedService(db)

@router.post("/experiments", response_model=QuantumMechanicsAdvancedExperimentResponse)
def create_experiment(exp_in: QuantumMechanicsAdvancedExperimentCreate, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[QuantumMechanicsAdvancedExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=QuantumMechanicsAdvancedExperimentResponse)
def get_experiment(experiment_id: int, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=QuantumMechanicsAdvancedExperimentResponse)
def update_experiment(experiment_id: int, exp_in: QuantumMechanicsAdvancedExperimentUpdate, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=QuantumMechanicsAdvancedFindingResponse)
def create_finding(finding_in: QuantumMechanicsAdvancedFindingCreate, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[QuantumMechanicsAdvancedFindingResponse])
def get_findings(experiment_id: int, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=QuantumMechanicsAdvancedDataPointResponse)
def create_datapoint(dp_in: QuantumMechanicsAdvancedDataPointCreate, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[QuantumMechanicsAdvancedDataPointResponse])
def get_datapoints(experiment_id: int, service: QuantumMechanicsAdvancedService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
