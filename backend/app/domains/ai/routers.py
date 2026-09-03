from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import AiExperimentCreate, AiExperimentUpdate, AiExperimentResponse, AiFindingCreate, AiFindingResponse, AiDataPointCreate, AiDataPointResponse
from .services import AiService

router = APIRouter(prefix="/ai", tags=["Ai"])

def get_service(db: Session = Depends(get_db)) -> AiService:
    return AiService(db)

@router.post("/experiments", response_model=AiExperimentResponse)
def create_experiment(exp_in: AiExperimentCreate, service: AiService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[AiExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: AiService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=AiExperimentResponse)
def get_experiment(experiment_id: int, service: AiService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=AiExperimentResponse)
def update_experiment(experiment_id: int, exp_in: AiExperimentUpdate, service: AiService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: AiService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=AiFindingResponse)
def create_finding(finding_in: AiFindingCreate, service: AiService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[AiFindingResponse])
def get_findings(experiment_id: int, service: AiService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=AiDataPointResponse)
def create_datapoint(dp_in: AiDataPointCreate, service: AiService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[AiDataPointResponse])
def get_datapoints(experiment_id: int, service: AiService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
