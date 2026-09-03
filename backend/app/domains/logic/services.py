from sqlalchemy.orm import Session
from .models import LogicExperiment, LogicFinding, LogicDataPoint
from .schemas import LogicExperimentCreate, LogicExperimentUpdate, LogicFindingCreate, LogicDataPointCreate
from typing import List, Optional

class LogicService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[LogicExperiment]:
        return self.db.query(LogicExperiment).filter(LogicExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[LogicExperiment]:
        return self.db.query(LogicExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: LogicExperimentCreate) -> LogicExperiment:
        db_exp = LogicExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: LogicExperimentUpdate) -> Optional[LogicExperiment]:
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

    def create_finding(self, finding_in: LogicFindingCreate) -> LogicFinding:
        db_finding = LogicFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[LogicFinding]:
        return self.db.query(LogicFinding).filter(LogicFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: LogicDataPointCreate) -> LogicDataPoint:
        db_dp = LogicDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[LogicDataPoint]:
        return self.db.query(LogicDataPoint).filter(LogicDataPoint.experiment_id == experiment_id).all()
