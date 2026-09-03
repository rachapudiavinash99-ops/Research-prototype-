from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import OpticsExperimentCreate, OpticsExperimentUpdate, OpticsExperimentResponse, OpticsFindingCreate, OpticsFindingResponse, OpticsDataPointCreate, OpticsDataPointResponse
from .services import OpticsService

router = APIRouter(prefix="/optics", tags=["Optics"])

def get_service(db: Session = Depends(get_db)) -> OpticsService:
    return OpticsService(db)

@router.post("/experiments", response_model=OpticsExperimentResponse)
def create_experiment(exp_in: OpticsExperimentCreate, service: OpticsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[OpticsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: OpticsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=OpticsExperimentResponse)
def get_experiment(experiment_id: int, service: OpticsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=OpticsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: OpticsExperimentUpdate, service: OpticsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: OpticsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=OpticsFindingResponse)
def create_finding(finding_in: OpticsFindingCreate, service: OpticsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[OpticsFindingResponse])
def get_findings(experiment_id: int, service: OpticsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=OpticsDataPointResponse)
def create_datapoint(dp_in: OpticsDataPointCreate, service: OpticsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[OpticsDataPointResponse])
def get_datapoints(experiment_id: int, service: OpticsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
