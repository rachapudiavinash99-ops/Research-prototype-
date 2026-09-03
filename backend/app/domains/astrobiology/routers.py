from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import AstrobiologyExperimentCreate, AstrobiologyExperimentUpdate, AstrobiologyExperimentResponse, AstrobiologyFindingCreate, AstrobiologyFindingResponse, AstrobiologyDataPointCreate, AstrobiologyDataPointResponse
from .services import AstrobiologyService

router = APIRouter(prefix="/astrobiology", tags=["Astrobiology"])

def get_service(db: Session = Depends(get_db)) -> AstrobiologyService:
    return AstrobiologyService(db)

@router.post("/experiments", response_model=AstrobiologyExperimentResponse)
def create_experiment(exp_in: AstrobiologyExperimentCreate, service: AstrobiologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[AstrobiologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: AstrobiologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=AstrobiologyExperimentResponse)
def get_experiment(experiment_id: int, service: AstrobiologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=AstrobiologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: AstrobiologyExperimentUpdate, service: AstrobiologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: AstrobiologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=AstrobiologyFindingResponse)
def create_finding(finding_in: AstrobiologyFindingCreate, service: AstrobiologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[AstrobiologyFindingResponse])
def get_findings(experiment_id: int, service: AstrobiologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=AstrobiologyDataPointResponse)
def create_datapoint(dp_in: AstrobiologyDataPointCreate, service: AstrobiologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[AstrobiologyDataPointResponse])
def get_datapoints(experiment_id: int, service: AstrobiologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
