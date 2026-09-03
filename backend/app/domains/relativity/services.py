from sqlalchemy.orm import Session
from .models import RelativityExperiment, RelativityFinding, RelativityDataPoint
from .schemas import RelativityExperimentCreate, RelativityExperimentUpdate, RelativityFindingCreate, RelativityDataPointCreate
from typing import List, Optional

class RelativityService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[RelativityExperiment]:
        return self.db.query(RelativityExperiment).filter(RelativityExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[RelativityExperiment]:
        return self.db.query(RelativityExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: RelativityExperimentCreate) -> RelativityExperiment:
        db_exp = RelativityExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: RelativityExperimentUpdate) -> Optional[RelativityExperiment]:
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

    def create_finding(self, finding_in: RelativityFindingCreate) -> RelativityFinding:
        db_finding = RelativityFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[RelativityFinding]:
        return self.db.query(RelativityFinding).filter(RelativityFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: RelativityDataPointCreate) -> RelativityDataPoint:
        db_dp = RelativityDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[RelativityDataPoint]:
        return self.db.query(RelativityDataPoint).filter(RelativityDataPoint.experiment_id == experiment_id).all()
