from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import IotExperimentCreate, IotExperimentUpdate, IotExperimentResponse, IotFindingCreate, IotFindingResponse, IotDataPointCreate, IotDataPointResponse
from .services import IotService

router = APIRouter(prefix="/iot", tags=["Iot"])

def get_service(db: Session = Depends(get_db)) -> IotService:
    return IotService(db)

@router.post("/experiments", response_model=IotExperimentResponse)
def create_experiment(exp_in: IotExperimentCreate, service: IotService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[IotExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: IotService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=IotExperimentResponse)
def get_experiment(experiment_id: int, service: IotService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=IotExperimentResponse)
def update_experiment(experiment_id: int, exp_in: IotExperimentUpdate, service: IotService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: IotService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=IotFindingResponse)
def create_finding(finding_in: IotFindingCreate, service: IotService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[IotFindingResponse])
def get_findings(experiment_id: int, service: IotService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=IotDataPointResponse)
def create_datapoint(dp_in: IotDataPointCreate, service: IotService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[IotDataPointResponse])
def get_datapoints(experiment_id: int, service: IotService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
