from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import AgronomyExperimentCreate, AgronomyExperimentUpdate, AgronomyExperimentResponse, AgronomyFindingCreate, AgronomyFindingResponse, AgronomyDataPointCreate, AgronomyDataPointResponse
from .services import AgronomyService

router = APIRouter(prefix="/agronomy", tags=["Agronomy"])

def get_service(db: Session = Depends(get_db)) -> AgronomyService:
    return AgronomyService(db)

@router.post("/experiments", response_model=AgronomyExperimentResponse)
def create_experiment(exp_in: AgronomyExperimentCreate, service: AgronomyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[AgronomyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: AgronomyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=AgronomyExperimentResponse)
def get_experiment(experiment_id: int, service: AgronomyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=AgronomyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: AgronomyExperimentUpdate, service: AgronomyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: AgronomyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=AgronomyFindingResponse)
def create_finding(finding_in: AgronomyFindingCreate, service: AgronomyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[AgronomyFindingResponse])
def get_findings(experiment_id: int, service: AgronomyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=AgronomyDataPointResponse)
def create_datapoint(dp_in: AgronomyDataPointCreate, service: AgronomyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[AgronomyDataPointResponse])
def get_datapoints(experiment_id: int, service: AgronomyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
