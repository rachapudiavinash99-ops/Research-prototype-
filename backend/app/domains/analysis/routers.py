from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from .schemas import AnalysisExperimentCreate, AnalysisExperimentUpdate, AnalysisExperimentResponse, AnalysisFindingCreate, AnalysisFindingResponse, AnalysisDataPointCreate, AnalysisDataPointResponse
from .services import AnalysisService

router = APIRouter(prefix="/analysis", tags=["Analysis"])

def get_service(db: Session = Depends(get_db)) -> AnalysisService:
    return AnalysisService(db)

@router.post("/experiments", response_model=AnalysisExperimentResponse)
def create_experiment(exp_in: AnalysisExperimentCreate, service: AnalysisService = Depends(get_service)):
    return service.create_experiment(exp_in)

@router.get("/experiments", response_model=List[AnalysisExperimentResponse])
def get_experiments(skip: int = 0, limit: int = 100, service: AnalysisService = Depends(get_service)):
    return service.get_experiments(skip=skip, limit=limit)

@router.get("/experiments/{experiment_id}", response_model=AnalysisExperimentResponse)
def get_experiment(experiment_id: int, service: AnalysisService = Depends(get_service)):
    exp = service.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.put("/experiments/{experiment_id}", response_model=AnalysisExperimentResponse)
def update_experiment(experiment_id: int, exp_in: AnalysisExperimentUpdate, service: AnalysisService = Depends(get_service)):
    exp = service.update_experiment(experiment_id, exp_in)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, service: AnalysisService = Depends(get_service)):
    if not service.delete_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"detail": "Deleted"}

@router.post("/findings", response_model=AnalysisFindingResponse)
def create_finding(finding_in: AnalysisFindingCreate, service: AnalysisService = Depends(get_service)):
    return service.create_finding(finding_in)

@router.get("/experiments/{experiment_id}/findings", response_model=List[AnalysisFindingResponse])
def get_findings(experiment_id: int, service: AnalysisService = Depends(get_service)):
    return service.get_findings(experiment_id)
    
@router.post("/datapoints", response_model=AnalysisDataPointResponse)
def create_datapoint(dp_in: AnalysisDataPointCreate, service: AnalysisService = Depends(get_service)):
    return service.create_datapoint(dp_in)

@router.get("/experiments/{experiment_id}/datapoints", response_model=List[AnalysisDataPointResponse])
def get_datapoints(experiment_id: int, service: AnalysisService = Depends(get_service)):
    return service.get_datapoints(experiment_id)
