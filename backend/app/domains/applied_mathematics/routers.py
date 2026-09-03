from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import AppliedMathematicsExperimentCreate, AppliedMathematicsExperimentUpdate, AppliedMathematicsExperimentResponse, AppliedMathematicsFindingCreate, AppliedMathematicsFindingResponse, AppliedMathematicsDataPointCreate, AppliedMathematicsDataPointResponse
from .services import AppliedMathematicsService

router = APIRouter(prefix="/applied_mathematics", tags=["AppliedMathematics"])

def get_service(db: Session = Depends(get_db)) -> AppliedMathematicsService:
    return AppliedMathematicsService(db)

@router.post("/experiments", response_model=AppliedMathematicsExperimentResponse)
def create_experiment(exp_in: AppliedMathematicsExperimentCreate, service: AppliedMathematicsService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[AppliedMathematicsExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: AppliedMathematicsService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=AppliedMathematicsExperimentResponse)
def get_experiment(experiment_id: int, service: AppliedMathematicsService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=AppliedMathematicsExperimentResponse)
def update_experiment(experiment_id: int, exp_in: AppliedMathematicsExperimentUpdate, service: AppliedMathematicsService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: AppliedMathematicsService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=AppliedMathematicsFindingResponse)
def create_finding(finding_in: AppliedMathematicsFindingCreate, service: AppliedMathematicsService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[AppliedMathematicsFindingResponse])
def get_findings(experiment_id: int, service: AppliedMathematicsService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=AppliedMathematicsDataPointResponse)
def create_datapoint(dp_in: AppliedMathematicsDataPointCreate, service: AppliedMathematicsService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[AppliedMathematicsDataPointResponse])
def get_datapoints(experiment_id: int, service: AppliedMathematicsService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
