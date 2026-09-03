from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import OperationsResearchExperimentCreate, OperationsResearchExperimentUpdate, OperationsResearchExperimentResponse, OperationsResearchFindingCreate, OperationsResearchFindingResponse, OperationsResearchDataPointCreate, OperationsResearchDataPointResponse
from .services import OperationsResearchService

router = APIRouter(prefix="/operations_research", tags=["OperationsResearch"])

def get_service(db: Session = Depends(get_db)) -> OperationsResearchService:
    return OperationsResearchService(db)

@router.post("/experiments", response_model=OperationsResearchExperimentResponse)
def create_experiment(exp_in: OperationsResearchExperimentCreate, service: OperationsResearchService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[OperationsResearchExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: OperationsResearchService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=OperationsResearchExperimentResponse)
def get_experiment(experiment_id: int, service: OperationsResearchService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=OperationsResearchExperimentResponse)
def update_experiment(experiment_id: int, exp_in: OperationsResearchExperimentUpdate, service: OperationsResearchService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: OperationsResearchService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=OperationsResearchFindingResponse)
def create_finding(finding_in: OperationsResearchFindingCreate, service: OperationsResearchService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[OperationsResearchFindingResponse])
def get_findings(experiment_id: int, service: OperationsResearchService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=OperationsResearchDataPointResponse)
def create_datapoint(dp_in: OperationsResearchDataPointCreate, service: OperationsResearchService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[OperationsResearchDataPointResponse])
def get_datapoints(experiment_id: int, service: OperationsResearchService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
