from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import SoftwareEngineeringExperimentCreate, SoftwareEngineeringExperimentUpdate, SoftwareEngineeringExperimentResponse, SoftwareEngineeringFindingCreate, SoftwareEngineeringFindingResponse, SoftwareEngineeringDataPointCreate, SoftwareEngineeringDataPointResponse
from .services import SoftwareEngineeringService

router = APIRouter(prefix="/software_engineering", tags=["SoftwareEngineering"])

def get_service(db: Session = Depends(get_db)) -> SoftwareEngineeringService:
    return SoftwareEngineeringService(db)

@router.post("/experiments", response_model=SoftwareEngineeringExperimentResponse)
def create_experiment(exp_in: SoftwareEngineeringExperimentCreate, service: SoftwareEngineeringService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[SoftwareEngineeringExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: SoftwareEngineeringService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=SoftwareEngineeringExperimentResponse)
def get_experiment(experiment_id: int, service: SoftwareEngineeringService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=SoftwareEngineeringExperimentResponse)
def update_experiment(experiment_id: int, exp_in: SoftwareEngineeringExperimentUpdate, service: SoftwareEngineeringService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: SoftwareEngineeringService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=SoftwareEngineeringFindingResponse)
def create_finding(finding_in: SoftwareEngineeringFindingCreate, service: SoftwareEngineeringService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[SoftwareEngineeringFindingResponse])
def get_findings(experiment_id: int, service: SoftwareEngineeringService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=SoftwareEngineeringDataPointResponse)
def create_datapoint(dp_in: SoftwareEngineeringDataPointCreate, service: SoftwareEngineeringService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[SoftwareEngineeringDataPointResponse])
def get_datapoints(experiment_id: int, service: SoftwareEngineeringService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
