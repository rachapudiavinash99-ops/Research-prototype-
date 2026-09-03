from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import SystemsPharmacologyExperimentCreate, SystemsPharmacologyExperimentUpdate, SystemsPharmacologyExperimentResponse, SystemsPharmacologyFindingCreate, SystemsPharmacologyFindingResponse, SystemsPharmacologyDataPointCreate, SystemsPharmacologyDataPointResponse
from .services import SystemsPharmacologyService

router = APIRouter(prefix="/systems_pharmacology", tags=["SystemsPharmacology"])

def get_service(db: Session = Depends(get_db)) -> SystemsPharmacologyService:
    return SystemsPharmacologyService(db)

@router.post("/experiments", response_model=SystemsPharmacologyExperimentResponse)
def create_experiment(exp_in: SystemsPharmacologyExperimentCreate, service: SystemsPharmacologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[SystemsPharmacologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: SystemsPharmacologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=SystemsPharmacologyExperimentResponse)
def get_experiment(experiment_id: int, service: SystemsPharmacologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=SystemsPharmacologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: SystemsPharmacologyExperimentUpdate, service: SystemsPharmacologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: SystemsPharmacologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=SystemsPharmacologyFindingResponse)
def create_finding(finding_in: SystemsPharmacologyFindingCreate, service: SystemsPharmacologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[SystemsPharmacologyFindingResponse])
def get_findings(experiment_id: int, service: SystemsPharmacologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=SystemsPharmacologyDataPointResponse)
def create_datapoint(dp_in: SystemsPharmacologyDataPointCreate, service: SystemsPharmacologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[SystemsPharmacologyDataPointResponse])
def get_datapoints(experiment_id: int, service: SystemsPharmacologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
