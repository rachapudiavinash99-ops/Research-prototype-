from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import ClimatologyExperimentCreate, ClimatologyExperimentUpdate, ClimatologyExperimentResponse, ClimatologyFindingCreate, ClimatologyFindingResponse, ClimatologyDataPointCreate, ClimatologyDataPointResponse
from .services import ClimatologyService

router = APIRouter(prefix="/climatology", tags=["Climatology"])

def get_service(db: Session = Depends(get_db)) -> ClimatologyService:
    return ClimatologyService(db)

@router.post("/experiments", response_model=ClimatologyExperimentResponse)
def create_experiment(exp_in: ClimatologyExperimentCreate, service: ClimatologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[ClimatologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: ClimatologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=ClimatologyExperimentResponse)
def get_experiment(experiment_id: int, service: ClimatologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=ClimatologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: ClimatologyExperimentUpdate, service: ClimatologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: ClimatologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=ClimatologyFindingResponse)
def create_finding(finding_in: ClimatologyFindingCreate, service: ClimatologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[ClimatologyFindingResponse])
def get_findings(experiment_id: int, service: ClimatologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=ClimatologyDataPointResponse)
def create_datapoint(dp_in: ClimatologyDataPointCreate, service: ClimatologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[ClimatologyDataPointResponse])
def get_datapoints(experiment_id: int, service: ClimatologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
