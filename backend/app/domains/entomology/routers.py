from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import EntomologyExperimentCreate, EntomologyExperimentUpdate, EntomologyExperimentResponse, EntomologyFindingCreate, EntomologyFindingResponse, EntomologyDataPointCreate, EntomologyDataPointResponse
from .services import EntomologyService

router = APIRouter(prefix="/entomology", tags=["Entomology"])

def get_service(db: Session = Depends(get_db)) -> EntomologyService:
    return EntomologyService(db)

@router.post("/experiments", response_model=EntomologyExperimentResponse)
def create_experiment(exp_in: EntomologyExperimentCreate, service: EntomologyService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[EntomologyExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: EntomologyService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=EntomologyExperimentResponse)
def get_experiment(experiment_id: int, service: EntomologyService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=EntomologyExperimentResponse)
def update_experiment(experiment_id: int, exp_in: EntomologyExperimentUpdate, service: EntomologyService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: EntomologyService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=EntomologyFindingResponse)
def create_finding(finding_in: EntomologyFindingCreate, service: EntomologyService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[EntomologyFindingResponse])
def get_findings(experiment_id: int, service: EntomologyService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=EntomologyDataPointResponse)
def create_datapoint(dp_in: EntomologyDataPointCreate, service: EntomologyService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[EntomologyDataPointResponse])
def get_datapoints(experiment_id: int, service: EntomologyService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
