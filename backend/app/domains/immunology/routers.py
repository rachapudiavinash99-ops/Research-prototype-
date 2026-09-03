from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import ImmunologyExperimentCreate, ImmunologyExperimentUpdate, ImmunologyExperimentResponse, ImmunologyFindingCreate, ImmunologyFindingResponse, ImmunologyDataPointCreate, ImmunologyDataPointResponse
from .services import ImmunologyService

router = APIRouter(prefix="/immunology", tags=["Immunology"])

def get_service(db: Session = Depends(get_db)) -> ImmunologyService:
    return ImmunologyService(db)

@router.post("/experiments", response_model=ImmunologyExperimentResponse)
def create_experiment(exp_in: ImmunologyExperimentCreate, service: ImmunologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[ImmunologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: ImmunologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=ImmunologyExperimentResponse)
def get_experiment(experiment_id: int, service: ImmunologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=ImmunologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: ImmunologyExperimentUpdate, service: ImmunologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: ImmunologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=ImmunologyFindingResponse)
def create_finding(finding_in: ImmunologyFindingCreate, service: ImmunologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[ImmunologyFindingResponse])
def get_findings(experiment_id: int, service: ImmunologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=ImmunologyDataPointResponse)
def create_datapoint(dp_in: ImmunologyDataPointCreate, service: ImmunologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[ImmunologyDataPointResponse])
def get_datapoints(experiment_id: int, service: ImmunologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
