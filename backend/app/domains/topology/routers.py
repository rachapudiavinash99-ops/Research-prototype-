from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import TopologyExperimentCreate, TopologyExperimentUpdate, TopologyExperimentResponse, TopologyFindingCreate, TopologyFindingResponse, TopologyDataPointCreate, TopologyDataPointResponse
from .services import TopologyService

router = APIRouter(prefix="/topology", tags=["Topology"])

def get_service(db: Session = Depends(get_db)) -> TopologyService:
    return TopologyService(db)

@router.post("/experiments", response_model=TopologyExperimentResponse)
def create_experiment(exp_in: TopologyExperimentCreate, service: TopologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[TopologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: TopologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=TopologyExperimentResponse)
def get_experiment(experiment_id: int, service: TopologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=TopologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: TopologyExperimentUpdate, service: TopologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: TopologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=TopologyFindingResponse)
def create_finding(finding_in: TopologyFindingCreate, service: TopologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[TopologyFindingResponse])
def get_findings(experiment_id: int, service: TopologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=TopologyDataPointResponse)
def create_datapoint(dp_in: TopologyDataPointCreate, service: TopologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[TopologyDataPointResponse])
def get_datapoints(experiment_id: int, service: TopologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
