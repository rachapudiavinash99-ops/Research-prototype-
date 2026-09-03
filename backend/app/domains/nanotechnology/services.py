from sqlalchemy.orm import Session
from .models import NanotechnologyExperiment, NanotechnologyFinding, NanotechnologyDataPoint
from .schemas import NanotechnologyExperimentCreate, NanotechnologyExperimentUpdate, NanotechnologyFindingCreate, NanotechnologyDataPointCreate
from typing import List, Optional

class NanotechnologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[NanotechnologyExperiment]:
        return self.db.query(NanotechnologyExperiment).filter(NanotechnologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[NanotechnologyExperiment]:
        return self.db.query(NanotechnologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: NanotechnologyExperimentCreate) -> NanotechnologyExperiment:
        db_exp = NanotechnologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: NanotechnologyExperimentUpdate) -> Optional[NanotechnologyExperiment]:
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

    def create_finding(self, finding_in: NanotechnologyFindingCreate) -> NanotechnologyFinding:
        db_finding = NanotechnologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[NanotechnologyFinding]:
        return self.db.query(NanotechnologyFinding).filter(NanotechnologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: NanotechnologyDataPointCreate) -> NanotechnologyDataPoint:
        db_dp = NanotechnologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[NanotechnologyDataPoint]:
        return self.db.query(NanotechnologyDataPoint).filter(NanotechnologyDataPoint.experiment_id == experiment_id).all()
