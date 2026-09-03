from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import HorticultureExperimentCreate, HorticultureExperimentUpdate, HorticultureExperimentResponse, HorticultureFindingCreate, HorticultureFindingResponse, HorticultureDataPointCreate, HorticultureDataPointResponse
from .services import HorticultureService

router = APIRouter(prefix="/horticulture", tags=["Horticulture"])

def get_service(db: Session = Depends(get_db)) -> HorticultureService:
    return HorticultureService(db)

@router.post("/experiments", response_model=HorticultureExperimentResponse)
def create_experiment(exp_in: HorticultureExperimentCreate, service: HorticultureService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[HorticultureExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: HorticultureService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=HorticultureExperimentResponse)
def get_experiment(experiment_id: int, service: HorticultureService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=HorticultureExperimentResponse)
def update_experiment(experiment_id: int, exp_in: HorticultureExperimentUpdate, service: HorticultureService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: HorticultureService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=HorticultureFindingResponse)
def create_finding(finding_in: HorticultureFindingCreate, service: HorticultureService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[HorticultureFindingResponse])
def get_findings(experiment_id: int, service: HorticultureService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=HorticultureDataPointResponse)
def create_datapoint(dp_in: HorticultureDataPointCreate, service: HorticultureService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[HorticultureDataPointResponse])
def get_datapoints(experiment_id: int, service: HorticultureService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
