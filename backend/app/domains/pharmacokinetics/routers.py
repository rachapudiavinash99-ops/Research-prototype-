from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import PharmacokineticsExperimentCreate, PharmacokineticsExperimentUpdate, PharmacokineticsExperimentResponse, PharmacokineticsFindingCreate, PharmacokineticsFindingResponse, PharmacokineticsDataPointCreate, PharmacokineticsDataPointResponse
from .services import PharmacokineticsService

router = APIRouter(prefix="/pharmacokinetics", tags=["Pharmacokinetics"])

def get_service(db: Session = Depends(get_db)) -> PharmacokineticsService:
    return PharmacokineticsService(db)

@router.post("/experiments", response_model=PharmacokineticsExperimentResponse)
def create_experiment(exp_in: PharmacokineticsExperimentCreate, service: PharmacokineticsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[PharmacokineticsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: PharmacokineticsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=PharmacokineticsExperimentResponse)
def get_experiment(experiment_id: int, service: PharmacokineticsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=PharmacokineticsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: PharmacokineticsExperimentUpdate, service: PharmacokineticsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: PharmacokineticsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=PharmacokineticsFindingResponse)
def create_finding(finding_in: PharmacokineticsFindingCreate, service: PharmacokineticsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[PharmacokineticsFindingResponse])
def get_findings(experiment_id: int, service: PharmacokineticsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=PharmacokineticsDataPointResponse)
def create_datapoint(dp_in: PharmacokineticsDataPointCreate, service: PharmacokineticsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[PharmacokineticsDataPointResponse])
def get_datapoints(experiment_id: int, service: PharmacokineticsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
