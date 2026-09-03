from sqlalchemy.orm import Session
from .models import HistoryExperiment, HistoryFinding, HistoryDataPoint
from .schemas import HistoryExperimentCreate, HistoryExperimentUpdate, HistoryFindingCreate, HistoryDataPointCreate
from typing import List, Optional

class HistoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[HistoryExperiment]:
        return self.db.query(HistoryExperiment).filter(HistoryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[HistoryExperiment]:
        return self.db.query(HistoryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: HistoryExperimentCreate) -> HistoryExperiment:
        db_exp = HistoryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: HistoryExperimentUpdate) -> Optional[HistoryExperiment]:
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

    def create_finding(self, finding_in: HistoryFindingCreate) -> HistoryFinding:
        db_finding = HistoryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[HistoryFinding]:
        return self.db.query(HistoryFinding).filter(HistoryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: HistoryDataPointCreate) -> HistoryDataPoint:
        db_dp = HistoryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[HistoryDataPoint]:
        return self.db.query(HistoryDataPoint).filter(HistoryDataPoint.experiment_id == experiment_id).all()
