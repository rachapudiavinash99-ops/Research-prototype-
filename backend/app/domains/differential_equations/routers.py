from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import DifferentialEquationsExperimentCreate, DifferentialEquationsExperimentUpdate, DifferentialEquationsExperimentResponse, DifferentialEquationsFindingCreate, DifferentialEquationsFindingResponse, DifferentialEquationsDataPointCreate, DifferentialEquationsDataPointResponse
from .services import DifferentialEquationsService

router = APIRouter(prefix="/differential_equations", tags=["DifferentialEquations"])

def get_service(db: Session = Depends(get_db)) -> DifferentialEquationsService:
    return DifferentialEquationsService(db)

@router.post("/experiments", response_model=DifferentialEquationsExperimentResponse)
def create_experiment(exp_in: DifferentialEquationsExperimentCreate, service: DifferentialEquationsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[DifferentialEquationsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: DifferentialEquationsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=DifferentialEquationsExperimentResponse)
def get_experiment(experiment_id: int, service: DifferentialEquationsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=DifferentialEquationsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: DifferentialEquationsExperimentUpdate, service: DifferentialEquationsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: DifferentialEquationsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=DifferentialEquationsFindingResponse)
def create_finding(finding_in: DifferentialEquationsFindingCreate, service: DifferentialEquationsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[DifferentialEquationsFindingResponse])
def get_findings(experiment_id: int, service: DifferentialEquationsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=DifferentialEquationsDataPointResponse)
def create_datapoint(dp_in: DifferentialEquationsDataPointCreate, service: DifferentialEquationsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[DifferentialEquationsDataPointResponse])
def get_datapoints(experiment_id: int, service: DifferentialEquationsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
