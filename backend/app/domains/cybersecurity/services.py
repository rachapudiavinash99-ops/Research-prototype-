from sqlalchemy.orm import Session
from .models import CybersecurityExperiment, CybersecurityFinding, CybersecurityDataPoint
from .schemas import CybersecurityExperimentCreate, CybersecurityExperimentUpdate, CybersecurityFindingCreate, CybersecurityDataPointCreate
from typing import List, Optional

class CybersecurityService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[CybersecurityExperiment]:
        return self.db.query(CybersecurityExperiment).filter(CybersecurityExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[CybersecurityExperiment]:
        return self.db.query(CybersecurityExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: CybersecurityExperimentCreate) -> CybersecurityExperiment:
        db_exp = CybersecurityExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: CybersecurityExperimentUpdate) -> Optional[CybersecurityExperiment]:
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

    def create_finding(self, finding_in: CybersecurityFindingCreate) -> CybersecurityFinding:
        db_finding = CybersecurityFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[CybersecurityFinding]:
        return self.db.query(CybersecurityFinding).filter(CybersecurityFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: CybersecurityDataPointCreate) -> CybersecurityDataPoint:
        db_dp = CybersecurityDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[CybersecurityDataPoint]:
        return self.db.query(CybersecurityDataPoint).filter(CybersecurityDataPoint.experiment_id == experiment_id).all()
