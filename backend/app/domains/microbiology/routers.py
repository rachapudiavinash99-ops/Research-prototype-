from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import MicrobiologyExperimentCreate, MicrobiologyExperimentUpdate, MicrobiologyExperimentResponse, MicrobiologyFindingCreate, MicrobiologyFindingResponse, MicrobiologyDataPointCreate, MicrobiologyDataPointResponse
from .services import MicrobiologyService

router = APIRouter(prefix="/microbiology", tags=["Microbiology"])

def get_service(db: Session = Depends(get_db)) -> MicrobiologyService:
    return MicrobiologyService(db)

@router.post("/experiments", response_model=MicrobiologyExperimentResponse)
def create_experiment(exp_in: MicrobiologyExperimentCreate, service: MicrobiologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[MicrobiologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: MicrobiologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=MicrobiologyExperimentResponse)
def get_experiment(experiment_id: int, service: MicrobiologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=MicrobiologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: MicrobiologyExperimentUpdate, service: MicrobiologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: MicrobiologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=MicrobiologyFindingResponse)
def create_finding(finding_in: MicrobiologyFindingCreate, service: MicrobiologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[MicrobiologyFindingResponse])
def get_findings(experiment_id: int, service: MicrobiologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=MicrobiologyDataPointResponse)
def create_datapoint(dp_in: MicrobiologyDataPointCreate, service: MicrobiologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[MicrobiologyDataPointResponse])
def get_datapoints(experiment_id: int, service: MicrobiologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
