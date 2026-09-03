from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import UrbanPlanningExperimentCreate, UrbanPlanningExperimentUpdate, UrbanPlanningExperimentResponse, UrbanPlanningFindingCreate, UrbanPlanningFindingResponse, UrbanPlanningDataPointCreate, UrbanPlanningDataPointResponse
from .services import UrbanPlanningService

router = APIRouter(prefix="/urban_planning", tags=["UrbanPlanning"])

def get_service(db: Session = Depends(get_db)) -> UrbanPlanningService:
    return UrbanPlanningService(db)

@router.post("/experiments", response_model=UrbanPlanningExperimentResponse)
def create_experiment(exp_in: UrbanPlanningExperimentCreate, service: UrbanPlanningService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[UrbanPlanningExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: UrbanPlanningService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=UrbanPlanningExperimentResponse)
def get_experiment(experiment_id: int, service: UrbanPlanningService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=UrbanPlanningExperimentResponse)
def update_experiment(experiment_id: int, exp_in: UrbanPlanningExperimentUpdate, service: UrbanPlanningService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: UrbanPlanningService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=UrbanPlanningFindingResponse)
def create_finding(finding_in: UrbanPlanningFindingCreate, service: UrbanPlanningService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[UrbanPlanningFindingResponse])
def get_findings(experiment_id: int, service: UrbanPlanningService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=UrbanPlanningDataPointResponse)
def create_datapoint(dp_in: UrbanPlanningDataPointCreate, service: UrbanPlanningService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[UrbanPlanningDataPointResponse])
def get_datapoints(experiment_id: int, service: UrbanPlanningService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
