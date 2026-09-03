from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import PolymerChemistryExperimentCreate, PolymerChemistryExperimentUpdate, PolymerChemistryExperimentResponse, PolymerChemistryFindingCreate, PolymerChemistryFindingResponse, PolymerChemistryDataPointCreate, PolymerChemistryDataPointResponse
from .services import PolymerChemistryService

router = APIRouter(prefix="/polymer_chemistry", tags=["PolymerChemistry"])

def get_service(db: Session = Depends(get_db)) -> PolymerChemistryService:
    return PolymerChemistryService(db)

@router.post("/experiments", response_model=PolymerChemistryExperimentResponse)
def create_experiment(exp_in: PolymerChemistryExperimentCreate, service: PolymerChemistryService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[PolymerChemistryExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: PolymerChemistryService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=PolymerChemistryExperimentResponse)
def get_experiment(experiment_id: int, service: PolymerChemistryService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=PolymerChemistryExperimentResponse)
def update_experiment(experiment_id: int, exp_in: PolymerChemistryExperimentUpdate, service: PolymerChemistryService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: PolymerChemistryService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=PolymerChemistryFindingResponse)
def create_finding(finding_in: PolymerChemistryFindingCreate, service: PolymerChemistryService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[PolymerChemistryFindingResponse])
def get_findings(experiment_id: int, service: PolymerChemistryService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=PolymerChemistryDataPointResponse)
def create_datapoint(dp_in: PolymerChemistryDataPointCreate, service: PolymerChemistryService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[PolymerChemistryDataPointResponse])
def get_datapoints(experiment_id: int, service: PolymerChemistryService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
