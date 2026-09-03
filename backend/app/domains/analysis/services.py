from sqlalchemy.orm import Session
from .models import AnalysisExperiment, AnalysisFinding, AnalysisDataPoint
from .schemas import AnalysisExperimentCreate, AnalysisExperimentUpdate, AnalysisFindingCreate, AnalysisDataPointCreate
from typing import List, Optional

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AnalysisExperiment]:
        return self.db.query(AnalysisExperiment).filter(AnalysisExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AnalysisExperiment]:
        return self.db.query(AnalysisExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AnalysisExperimentCreate) -> AnalysisExperiment:
        db_exp = AnalysisExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AnalysisExperimentUpdate) -> Optional[AnalysisExperiment]:
        db_exp = self.get_experiment(experiment_id)
        if not db_exp:
            return None
        update_data = exp_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_exp, field, value)
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def delete_experiment(self, experiment_id: int) -> bool:
        db_exp = self.get_experiment(experiment_id)
        if not db_exp:
            return False
        self.db.delete(db_exp)
        self.db.commit()
        return True

    def create_finding(self, finding_in: AnalysisFindingCreate) -> AnalysisFinding:
        db_finding = AnalysisFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AnalysisFinding]:
        return self.db.query(AnalysisFinding).filter(AnalysisFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AnalysisDataPointCreate) -> AnalysisDataPoint:
        db_dp = AnalysisDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AnalysisDataPoint]:
        return self.db.query(AnalysisDataPoint).filter(AnalysisDataPoint.experiment_id == experiment_id).all()
