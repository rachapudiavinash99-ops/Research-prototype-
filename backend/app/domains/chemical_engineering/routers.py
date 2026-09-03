from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import ChemicalEngineeringExperimentCreate, ChemicalEngineeringExperimentUpdate, ChemicalEngineeringExperimentResponse, ChemicalEngineeringFindingCreate, ChemicalEngineeringFindingResponse, ChemicalEngineeringDataPointCreate, ChemicalEngineeringDataPointResponse
from .services import ChemicalEngineeringService

router = APIRouter(prefix="/chemical_engineering", tags=["ChemicalEngineering"])

def get_service(db: Session = Depends(get_db)) -> ChemicalEngineeringService:
    return ChemicalEngineeringService(db)

@router.post("/experiments", response_model=ChemicalEngineeringExperimentResponse)
def create_experiment(exp_in: ChemicalEngineeringExperimentCreate, service: ChemicalEngineeringService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[ChemicalEngineeringExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: ChemicalEngineeringService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=ChemicalEngineeringExperimentResponse)
def get_experiment(experiment_id: int, service: ChemicalEngineeringService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=ChemicalEngineeringExperimentResponse)
def update_experiment(experiment_id: int, exp_in: ChemicalEngineeringExperimentUpdate, service: ChemicalEngineeringService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: ChemicalEngineeringService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=ChemicalEngineeringFindingResponse)
def create_finding(finding_in: ChemicalEngineeringFindingCreate, service: ChemicalEngineeringService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[ChemicalEngineeringFindingResponse])
def get_findings(experiment_id: int, service: ChemicalEngineeringService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=ChemicalEngineeringDataPointResponse)
def create_datapoint(dp_in: ChemicalEngineeringDataPointCreate, service: ChemicalEngineeringService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[ChemicalEngineeringDataPointResponse])
def get_datapoints(experiment_id: int, service: ChemicalEngineeringService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
